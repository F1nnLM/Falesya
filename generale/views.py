from django.shortcuts import render, get_object_or_404
from .models import Falesia, Percorso

# Lista ordinata dei gradi francesi — usata per il filtraggio per range
GRADI_ORDINATI = [
    '1', '2', '3',
    '4a', '4b', '4c',
    '5a', '5b', '5c',
    '6a', '6a+', '6b', '6b+', '6c', '6c+',
    '7a', '7a+', '7b', '7b+', '7c', '7c+',
    '8a', '8a+', '8b', '8b+', '8c', '8c+',
]

REGIONI_ITALIANE = [
    'Abruzzo', 'Basilicata', 'Calabria', 'Campania', 'Emilia-Romagna',
    'Friuli-Venezia Giulia', 'Lazio', 'Liguria', 'Lombardia', 'Marche',
    'Molise', 'Piemonte', 'Puglia', 'Sardegna', 'Sicilia',
    'Toscana', 'Trentino-Alto Adige', 'Umbria', "Valle d'Aosta", 'Veneto',
]


def home(request):
    return render(request, 'generale/home.html', {
        'gradi': GRADI_ORDINATI,
        'regioni': REGIONI_ITALIANE,
    })


def risultati(request):
    query        = request.GET.get('q', '')
    regione      = request.GET.get('regione', '')
    grado_min    = request.GET.get('grado_min', '')
    grado_max    = request.GET.get('grado_max', '')
    tipo_percorso = request.GET.get('tipo_percorso', '')
    ordine       = request.GET.get('ordine', 'nome')

    falesie  = Falesia.objects.all()
    percorsi = Percorso.objects.all()

    # --- filtro per nome ---
    if query:
        falesie  = falesie.filter(nome__icontains=query)
        percorsi = percorsi.filter(nome__icontains=query)

    # --- filtro per regione (solo falesie) ---
    if regione:
        falesie  = falesie.filter(regione__iexact=regione)
        # i percorsi appartengono a falesie: filtriamo via FK
        percorsi = percorsi.filter(falesia__regione__iexact=regione)

    # --- filtro per range grado (solo percorsi) ---
    if grado_min or grado_max:
        idx_min = GRADI_ORDINATI.index(grado_min) if grado_min in GRADI_ORDINATI else 0
        idx_max = GRADI_ORDINATI.index(grado_max) if grado_max in GRADI_ORDINATI else len(GRADI_ORDINATI) - 1
        gradi_validi = GRADI_ORDINATI[idx_min: idx_max + 1]
        percorsi = percorsi.filter(grado__in=gradi_validi)

    # --- filtro per tipo percorso ---
    if tipo_percorso:
        percorsi = percorsi.filter(tipo=tipo_percorso)
        falesie  = Falesia.objects.none()   # se filtri per tipo percorso non ha senso mostrare falesie

    # --- ordinamento ---
    if ordine == 'grado':
        # ordinamento personalizzato per grado: annotiamo la posizione nella lista
        from django.db.models import Case, When, IntegerField
        order_cases = [When(grado=g, then=i) for i, g in enumerate(GRADI_ORDINATI)]
        percorsi = percorsi.annotate(
            ordine_grado=Case(*order_cases, output_field=IntegerField())
        ).order_by('ordine_grado')
        falesie = falesie.order_by('nome')
    else:
        falesie  = falesie.order_by('nome')
        percorsi = percorsi.order_by('nome')

    return render(request, 'generale/risultati.html', {
        'falesie':       falesie,
        'percorsi':      percorsi,
        'query':         query,
        'regione':       regione,
        'grado_min':     grado_min,
        'grado_max':     grado_max,
        'tipo_percorso': tipo_percorso,
        'ordine':        ordine,
        'gradi':         GRADI_ORDINATI,
        'regioni':       REGIONI_ITALIANE,
    })


def dettaglio_falesia(request, id):
    falesia  = get_object_or_404(Falesia, id=id)
    percorsi = falesia.percorsi.all()
    commenti = falesia.commento_set.all()
    return render(request, 'generale/dettaglio_falesia.html', {
        'falesia':  falesia,
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