from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('risultati/', views.risultati, name='risultati'),
    path('falesia/<int:id>/', views.dettaglio_falesia, name='dettaglio_falesia'),
    path('percorso/<int:id>/', views.dettaglio_percorso, name='dettaglio_percorso'),
]