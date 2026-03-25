from django.urls import path
from .views import profilo_utente

app_name = 'utenti'

urlpatterns = [
    path('profilo/', profilo_utente, name='profilo'),
]