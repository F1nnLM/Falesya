from django.shortcuts import render
from django.contrib.auth.decorators import login_required

@login_required
def profilo_utente(request):
    return render(request, 'utenti/profilo.html')