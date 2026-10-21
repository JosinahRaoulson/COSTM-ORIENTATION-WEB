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
    # Formation et identité de base
    formation = models.ForeignKey('Formation', on_delete=models.SET_NULL, null=True, blank=True)
    
    # Nouveaux champs pour compléter la fiche PDF
    CIVILITE_CHOICES = [
        ('M.', 'M.'),
        ('Mme', 'Mme'),
        ('Mlle', 'Mlle'),
    ]
    civilite = models.CharField(max_length=10, choices=CIVILITE_CHOICES, blank=True, null=True)
    
    nom = models.CharField(max_length=100)
    prenom = models.CharField(max_length=100)
    
    date_naissance = models.DateField(blank=True, null=True)
    lieu_naissance = models.CharField(max_length=150, blank=True, null=True)
    domicile = models.CharField(max_length=255, blank=True, null=True)
    
    email = models.EmailField(blank=True, null=True)
    telephone = models.CharField(max_length=20, blank=True, null=True)
    tel_telma = models.CharField(max_length=20, blank=True, null=True)
    tel_orange = models.CharField(max_length=20, blank=True, null=True)
    tel_airtel = models.CharField(max_length=20, blank=True, null=True)
    
    # Horaire souhaité
    horaire = models.CharField(max_length=50, blank=True, null=True)
    
    # Mode de paiement (Exemple pour 2 versements)
    date_paiement_1 = models.DateField(blank=True, null=True)
    montant_1 = models.CharField(max_length=50, blank=True, null=True)
    date_paiement_2 = models.DateField(blank=True, null=True)
    montant_2 = models.CharField(max_length=50, blank=True, null=True)
    
    photo = models.ImageField(upload_to='photos_inscriptions/', blank=True, null=True)
    date_inscription = models.DateTimeField(auto_now_add=True)
    @property
    def photo_path_safe(self):
        if self.photo:
            # Remplace les antislashs Windows par des slashs standards
            return self.photo.path.replace('\\', '/')
        return ''

    def __str__(self):
        return f"{self.nom} {self.prenom}"
    





class Reponse(models.Model):
    question = models.ForeignKey(Question, on_delete=models.CASCADE, related_name="reponses")
    lettre = models.CharField(max_length=1)
    texte = models.CharField(max_length=255)
    formation = models.ForeignKey(Formation, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.lettre}. {self.texte}"