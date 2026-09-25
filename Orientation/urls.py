
from django.urls import path
from . import views
from .views import generer_pdf_inscription

urlpatterns = [
    
    path('', views.accueil_utilisateur, name='accueil_utilisateur'),
    path('formations/', views.liste_formations, name='liste_formations'),
    path('questionnaire/', views.questionnaire, name='questionnaire'),
    path('resultat/', views.resultat, name='resultat'),
    path('inscription/', views.inscription, name='inscription'),
    path('inscription/pdf/', generer_pdf_inscription, name='telecharger_pdf_inscription'),
    path('formation/<int:pk>/', views.detail_formation, name='detail_formation'),
]



