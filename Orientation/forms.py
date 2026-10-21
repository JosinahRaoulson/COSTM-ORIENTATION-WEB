from django import forms
from .models import QuestionPreliminaire, Question, Reponse, Inscription

class QuestionnaireForm(forms.Form):
    # Field pour la question préliminaire
    niveau_bureautique = forms.ChoiceField(
        label="Quel est votre niveau en informatique bureautique ?",
        choices=QuestionPreliminaire.NIVEAU_CHOICES,
        widget=forms.RadioSelect,
        required=True
    )

    # Dynamic creation of fields for the 20 questions
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        questions = Question.objects.all().order_by('ordre')
        
        for q in questions:
            choices = [(r.id, r.texte) for r in q.reponses.all()]
            self.fields[f'question_{q.id}'] = forms.ChoiceField(
                label=q.texte,
                choices=choices,
                widget=forms.RadioSelect,
                required=True
            )
class InscriptionForm(forms.ModelForm):
    class Meta:
        model = Inscription
        fields = '__all__'
        exclude = ['formation']