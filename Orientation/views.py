from django.shortcuts import render
from .models import Formation
from .models import Question
from django.shortcuts import render, redirect
from .models import Question, Reponse, Formation
from .models import Question, QuestionPreliminaire, Formation, Inscription

def accueil_utilisateur(request):
    return render(request, 'utilisateur/accueil.html')

def liste_formations(request):
    formations = Formation.objects.all()
    return render(request, 'utilisateur/formations.html', {'formations': formations})


def questionnaire(request):
    if request.method == 'POST':
        # On parcourt tout ce qui a été envoyé pour trouver les réponses aux questions
        for key, value in request.POST.items():
            if key.startswith('question_'):
                reponse_id = value
                try:
                    reponse_choisie = Reponse.objects.get(id=reponse_id)
                    # On enregistre l'ID de la formation associée dans la session
                    request.session['formation_id'] = reponse_choisie.formation.id
                except Reponse.DoesNotExist:
                    pass
        return redirect('resultat')

    questions = Question.objects.all().prefetch_related('reponses')
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
    
    # Si on passe l'ID dans l'URL ou qu'il est stocké en session
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
        # Traitement de ton formulaire d'inscription ici
        # (pense à lier l'inscription à la variable 'formation' récupérée)
        pass

    return render(request, 'utilisateur/inscription.html', {
        'formation': formation
    })
from django.http import HttpResponse
from django.template.loader import get_template
from xhtml2pdf import pisa

def generer_pdf_inscription(request):
    inscription = Inscription.objects.last()
    formation = inscription.formation if inscription else None

    context = {
        'inscription': inscription,
        'formation': formation,
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