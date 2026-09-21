from django.shortcuts import render, redirect
from .forms import QuestionnaireForm
from .models import Reponse, Formation

def questionnaire_view(request):
    if request.method == 'POST':
        form = QuestionnaireForm(request.POST)
        if form.is_valid():
            niveau = form.cleaned_data['niveau_bureautique']
            
            # Redirection vers bureautique si le niveau est débutant
            if niveau == 'DEB':
                return render(request, 'orientation/resultat.html', {
                    'message': "Nous vous conseillons de suivre d'abord une formation en Bureautique."
                })

            # Calcul des points par formation selon les réponses choisies
            scores = {}
            for key, reponse_id in form.cleaned_data.items():
                if key.startswith('question_'):
                    reponse = Reponse.objects.get(id=reponse_id)
                    formation = reponse.formation
                    if formation:
                        scores[formation] = scores.get(formation, 0) + 1

            # Trouver la formation avec le score le plus élevé
            formation_recommandee = max(scores, key=scores.get) if scores else None

            return render(request, 'orientation/resultat.html', {
                'formation': formation_recommandee
            })
    else:
        form = QuestionnaireForm()

    return render(request, 'orientation/questionnaire.html', {'form': form})