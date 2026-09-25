from django.db import models

class Formation(models.Model):
    nom = models.CharField(max_length=100)
    description = models.TextField()

    def __str__(self):
        return self.nom


class Question(models.Model):
    texte = models.CharField(max_length=255)
    ordre = models.IntegerField(default=0)

    def __str__(self):
        return self.texte


class QuestionPreliminaire(models.Model) :
    NIVEAU_CHOICES = [
       ('DEB', 'Débutant(e)'),
       ('INT', 'Intermédiaire'),
       ('AVA', 'Avancé(e)'),
       ('EXP', 'Expert(e)'),
    ]
    texte = models.CharField(max_length=255, default="Quel est votre niveau en informatique bureautique ?")

    def __str__(self):
        return self.texte


class Inscription(models.Model):
    formation = models.ForeignKey('Formation', on_delete=models.CASCADE)
    nom = models.CharField(max_length=100)
    prenom = models.CharField(max_length=100)
    email = models.EmailField()
    telephone = models.CharField(max_length=20)
    photo = models.ImageField(upload_to='photos_inscriptions/')
    date_inscription = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.nom} {self.prenom}"
    





class Reponse(models.Model):
    question = models.ForeignKey(Question, on_delete=models.CASCADE, related_name="reponses")
    lettre = models.CharField(max_length=1)
    texte = models.CharField(max_length=255)
    formation = models.ForeignKey(Formation, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.lettre}. {self.texte}"