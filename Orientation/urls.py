from django.contrib import admin
from django.urls import path, include
from . import views
from .views import generer_pdf_inscription
from django.conf import settings
from django.conf.urls.static import static
urlpatterns = [
    
    path('', views.accueil_utilisateur, name='accueil_utilisateur'),
    path('formations/', views.liste_formations, name='liste_formations'),
    path('questionnaire/', views.questionnaire, name='questionnaire'),
    path('resultat/', views.resultat, name='resultat'),
    path('inscription/', views.inscription, name='inscription'),
    path('inscription/pdf/', generer_pdf_inscription, name='telecharger_pdf_inscription'),
    path('formation/<int:pk>/', views.detail_formation, name='detail_formation'),
    path('inscription/<int:formation_id>/', views.inscription, name='inscription_avec_formation'),
    path('inscription/succes/', views.succes_inscription, name='succes_inscription'),
    path('generer-pdf-inscription/', views.generer_pdf_inscription, name='generer_pdf_inscription'),
]
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)


