from django.urls import path
from . import views

urlpatterns = [
    # Pagine principali
    path('', views.home, name='home'),
    path('risultati/', views.risultati, name='risultati'),
    path('falesia/<int:id>/', views.dettaglio_falesia, name='dettaglio_falesia'),
    path('percorso/<int:id>/', views.dettaglio_percorso, name='dettaglio_percorso'),

    # Autenticazione
    path('login/', views.vista_login, name='login'),
    path('logout/', views.vista_logout, name='logout'),
    path('registrazione/', views.vista_registrazione, name='registrazione'),

    # Profilo
    path('profilo/', views.vista_profilo, name='profilo'),

    # Commenti
    path('commento/<int:id>/elimina/', views.elimina_commento, name='elimina_commento'),
    # Preferiti
    path('preferito/toggle/', views.toggle_preferito, name='toggle_preferito'),
    #mappa
    path('mappa/', views.mappa, name='mappa'),
]
