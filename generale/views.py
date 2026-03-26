from django.shortcuts import render, get_object_or_404
from .models import Falesia, Percorso

def home(request):
    return render(request, 'generale/home.html')

def risultati(request):
    query = request.GET.get('q', '')
    tipo = request.GET.get('tipo', '')
    
    falesie = Falesia.objects.all()
    percorsi = Percorso.objects.all()
    
    if query:
        falesie = falesie.filter(nome__icontains=query)
        percorsi = percorsi.filter(nome__icontains=query)
    
    if tipo == 'falesia':
        percorsi = Percorso.objects.none()
    elif tipo == 'percorso':
        falesie = Falesia.objects.none()

    return render(request, 'generale/risultati.html', {
        'falesie': falesie,
        'percorsi': percorsi,
        'query': query,
    })

def dettaglio_falesia(request, id):
    falesia = get_object_or_404(Falesia, id=id)
    percorsi = falesia.percorsi.all()
    commenti = falesia.commento_set.all()
    return render(request, 'generale/dettaglio_falesia.html', {
        'falesia': falesia,
        'percorsi': percorsi,
        'commenti': commenti,
    })

def dettaglio_percorso(request, id):
    percorso = get_object_or_404(Percorso, id=id)
    commenti = percorso.commento_set.all()
    return render(request, 'generale/dettaglio_percorso.html', {
        'percorso': percorso,
        'commenti': commenti,
    })