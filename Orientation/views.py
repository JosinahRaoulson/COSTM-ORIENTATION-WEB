from django.shortcuts import render
from .models import Formation
from .models import Question
from django.shortcuts import render, redirect
from .models import Question, Reponse, Formation
from .models import Question, QuestionPreliminaire, Formation, Inscription
from django.template.loader import get_template
from django.http import HttpResponse
from xhtml2pdf import pisa
from .forms import InscriptionForm
import random

def accueil_utilisateur(request):
    return render(request, 'utilisateur/accueil.html')

def liste_formations(request):
    formations = Formation.objects.all()
    return render(request, 'utilisateur/formations.html', {'formations': formations})



def questionnaire(request):
    # 1. Sélection aléatoire de 10 questions au début d'une session ou lors d'un GET
    if 'questions_ids' not in request.session or request.method == 'GET':
        toutes_les_questions = list(Question.objects.values_list('id', flat=True))
        # On en choisit 10 au hasard (ou toutes si la base en contient moins de 10)
        nombre_a_choisir = min(10, len(toutes_les_questions))
        questions_selectionnees_ids = random.sample(toutes_les_questions, nombre_a_choisir)
        request.session['questions_ids'] = questions_selectionnees_ids
    else:
        questions_selectionnees_ids = request.session['questions_ids']

    # On récupère uniquement ces 10 questions pour les afficher
    questions = Question.objects.filter(id__in=questions_selectionnees_ids).prefetch_related('reponses')
    # Pour conserver l'ordre aléatoire dans la liste des questions
    questions = sorted(questions, key=lambda q: questions_selectionnees_ids.index(q.id))

    if request.method == 'POST':
        # --- On vérifie si toutes les 10 questions affichées ont une réponse ---
        toutes_repondues = True
        for question in questions:
            if not request.POST.get(f'question_{question.id}'):
                toutes_repondues = False
                break
        
        # Si une question manque, on bloque et on réaffiche les mêmes 10 questions avec l'erreur
        if not toutes_repondues:
            return render(request, 'utilisateur/questionnaire.html', {
                'questions': questions,
                'erreur': "Veuillez répondre à toutes les questions avant de continuer."
            })
        
        # Si tout est rempli, on traite les réponses
        for key, value in request.POST.items():
            if key.startswith('question_'):
                reponse_id = value
                try:
                    reponse_choisie = Reponse.objects.get(id=reponse_id)
                    request.session['formation_id'] = reponse_choisie.formation.id
                except Reponse.DoesNotExist:
                    pass
                    
        # Nettoyage de la session pour les prochains tests
        if 'questions_ids' in request.session:
            del request.session['questions_ids']
            
        return redirect('resultat')

    return render(request, 'utilisateur/questionnaire.html', {'questions': questions})
   
def resultat(request):
    formation_id = request.session.get('formation_id')
    formation = None
    pourcentage = 0  # Valeur par défaut
    
    if formation_id:
        try:
            formation = Formation.objects.get(id=formation_id)
            # Tu peux mettre un pourcentage fixe ou le calculer selon ta logique
            pourcentage = 90  # Par exemple 90% de compatibilité
        except Formation.DoesNotExist:
            pass
            
    return render(request, 'utilisateur/resultat.html', {
        'formation': formation,
        'pourcentage': pourcentage
    })

def resultat(request):
    formation_id = request.session.get('formation_id')
    formation = None
    pourcentage = 85  # Tu peux mettre une valeur fixe pour l'instant (ex: 85)
    
    if formation_id:
        try:
            formation = Formation.objects.get(id=formation_id)
        except Formation.DoesNotExist:
            pass
            
    return render(request, 'utilisateur/resultat.html', {
        'formation': formation,
        'pourcentage': pourcentage
    })
def inscription(request, formation_id=None):
    formation = None
    
    if formation_id:
        try:
            formation = Formation.objects.get(id=formation_id)
        except Formation.DoesNotExist:
            pass
    elif 'formation_id' in request.session:
        try:
            formation = Formation.objects.get(id=request.session['formation_id'])
        except Formation.DoesNotExist:
            pass

    if request.method == 'POST':
        form = InscriptionForm(request.POST, request.FILES)
        if form.is_valid():
            inscription_obj = form.save(commit=False)
            if formation:
                inscription_obj.formation = formation
            inscription_obj.save()
            
            # 1. On stocke l'ID en session pour identifier cet étudiant précis
            request.session['inscription_id'] = inscription_obj.id
            
            # 2. SOLUTION DIRECTE : Au lieu d'aller sur une page de succès, 
            # on déclenche directement la vue de génération du PDF !
            return redirect('generer_pdf_inscription')
    else:
        form = InscriptionForm()

    return render(request, 'utilisateur/inscription.html', {
        'form': form,
        'formation': formation
    })
    
import os

import base64

def generer_pdf_inscription(request):
    inscription_id = request.session.get('inscription_id')
    if inscription_id:
        inscription = Inscription.objects.filter(id=inscription_id).first()
    else:
        inscription = Inscription.objects.last()

    formation = inscription.formation if inscription else None

    # Conversion de la photo en Base64
    photo_base64 = None
    if inscription and inscription.photo:
        try:
            # inscription.photo.path donne le chemin complet sur le disque dur
            with open(inscription.photo.path, "rb") as image_file:
                encoded = base64.b64encode(image_file.read()).decode('utf-8')
                # On détecte l'extension (jpg, png, etc.)
                ext = inscription.photo.name.split('.')[-1].lower()
                if ext == 'jpg':
                    ext = 'jpeg'
                photo_base64 = f"data:image/{ext};base64,{encoded}"
        except Exception as e:
            print(f"Erreur photo PDF : {e}")

    context = {
        'inscription': inscription,
        'formation': formation,
        'photo_base64': photo_base64, # Important : on transmet bien cette variable
        'request': request,
    }
    
    template_path = 'utilisateur/pdf_inscription.html'
    template = get_template(template_path)
    html = template.render(context)

    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = 'attachment; filename="fiche_inscription_costm.pdf"'

    pisa_status = pisa.CreatePDF(html, dest=response)

    if pisa_status.err:
        return HttpResponse(f'Erreur lors de la génération <pre>{html}</pre>')
    return response
   
def detail_formation(request, pk):
    try:
        formation = Formation.objects.get(pk=pk)
    except Formation.DoesNotExist:
        formation = None
    return render(request, 'utilisateur/detail_formation.html', {'formation': formation})

def succes_inscription(request):
    return render(request, 'utilisateur/succes.html')

import os
from django.conf import settings



def link_callback(uri, rel):
    sUrl = settings.STATIC_URL
    sRoot = settings.STATIC_ROOT
    mUrl = settings.MEDIA_URL
    mRoot = settings.MEDIA_ROOT

    if uri.startswith(mUrl):
        path = os.path.join(mRoot, uri.replace(mUrl, ""))
    elif uri.startswith(sUrl):
        path = os.path.join(sRoot, uri.replace(sUrl, ""))
    else:
        return uri

    # --- DIAGNOSTIC ---
    print(f"URI cherchée : {uri}")
    print(f"Chemin absolu généré : {path}")
    print(f"Le fichier existe ? {os.path.isfile(path)}")
    # ------------------

    if not os.path.isfile(path):
        return uri
    return path