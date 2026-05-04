from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth import login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import AuthenticationForm
from django.contrib import messages
from django.db.models import Avg

from django.contrib.auth.models import User
from .models import Falesia, Percorso, Commento, Valutazione
from .forms import FormRegistrazione, FormCommento, FormValutazione, FormProfiloImmagine, FormDatiUtente, FormCambioPassword

# ── COSTANTI ──────────────────────────────────────────────────────────────────

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


# ── HOME ──────────────────────────────────────────────────────────────────────

def home(request):
    return render(request, 'generale/home.html', {
        'gradi': GRADI_ORDINATI,
        'regioni': REGIONI_ITALIANE,
    })


# ── RICERCA / FILTRI ──────────────────────────────────────────────────────────

def risultati(request):
    query         = request.GET.get('q', '')
    regione       = request.GET.get('regione', '')
    grado_min     = request.GET.get('grado_min', '')
    grado_max     = request.GET.get('grado_max', '')
    tipo_percorso = request.GET.get('tipo_percorso', '')
    ordine        = request.GET.get('ordine', 'nome')

    falesie  = Falesia.objects.all()
    percorsi = Percorso.objects.all()

    if query:
        falesie  = falesie.filter(nome__icontains=query)
        percorsi = percorsi.filter(nome__icontains=query)

    if regione:
        falesie  = falesie.filter(regione__iexact=regione)
        percorsi = percorsi.filter(falesia__regione__iexact=regione)

    if grado_min or grado_max:
        idx_min = GRADI_ORDINATI.index(grado_min) if grado_min in GRADI_ORDINATI else 0
        idx_max = GRADI_ORDINATI.index(grado_max) if grado_max in GRADI_ORDINATI else len(GRADI_ORDINATI) - 1
        gradi_validi = GRADI_ORDINATI[idx_min: idx_max + 1]
        percorsi = percorsi.filter(grado__in=gradi_validi)

    if tipo_percorso:
        percorsi = percorsi.filter(tipo=tipo_percorso)
        falesie  = Falesia.objects.none()

    if ordine == 'grado':
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
        'falesie':        falesie,
        'percorsi':       percorsi,
        'query':          query,
        'regione':        regione,
        'grado_min':      grado_min,
        'grado_max':      grado_max,
        'tipo_percorso':  tipo_percorso,
        'ordine':         ordine,
        'gradi':          GRADI_ORDINATI,
        'regioni':        REGIONI_ITALIANE,
    })


# ── DETTAGLIO FALESIA ─────────────────────────────────────────────────────────

def dettaglio_falesia(request, id):
    falesia  = get_object_or_404(Falesia, id=id)
    percorsi = falesia.percorsi.all()
    commenti = falesia.commento_set.select_related('utente__profilo').order_by('-data')

    media_voto = Valutazione.objects.filter(falesia=falesia).aggregate(Avg('voto'))['voto__avg']

    voto_utente = None
    if request.user.is_authenticated:
        v = Valutazione.objects.filter(utente=request.user, falesia=falesia).first()
        voto_utente = v.voto if v else None

    form_commento    = FormCommento()
    form_valutazione = FormValutazione()

    if request.method == 'POST' and request.user.is_authenticated:

        if 'invia_commento' in request.POST:
            form_commento = FormCommento(request.POST)
            if form_commento.is_valid():
                c = form_commento.save(commit=False)
                c.utente  = request.user
                c.falesia = falesia
                c.save()
                messages.success(request, 'Commento pubblicato.')
                return redirect('dettaglio_falesia', id=id)

        elif 'invia_valutazione' in request.POST:
            esistente = Valutazione.objects.filter(utente=request.user, falesia=falesia).first()
            form_valutazione = FormValutazione(request.POST, instance=esistente)
            if form_valutazione.is_valid():
                v = form_valutazione.save(commit=False)
                v.utente  = request.user
                v.falesia = falesia
                v.save()
                messages.success(request, 'Valutazione salvata.')
                return redirect('dettaglio_falesia', id=id)

    return render(request, 'generale/dettaglio_falesia.html', {
        'falesia':          falesia,
        'percorsi':         percorsi,
        'commenti':         commenti,
        'media_voto':       media_voto,
        'media_voto_int':   round(media_voto) if media_voto else 0,
        'voto_utente':      voto_utente,
        'form_commento':    form_commento,
        'form_valutazione': form_valutazione,
    })


# ── DETTAGLIO PERCORSO ────────────────────────────────────────────────────────

def dettaglio_percorso(request, id):
    percorso = get_object_or_404(Percorso, id=id)
    commenti = percorso.commento_set.select_related('utente__profilo').order_by('-data')

    media_voto = Valutazione.objects.filter(percorso=percorso).aggregate(Avg('voto'))['voto__avg']

    voto_utente = None
    if request.user.is_authenticated:
        v = Valutazione.objects.filter(utente=request.user, percorso=percorso).first()
        voto_utente = v.voto if v else None

    form_commento    = FormCommento()
    form_valutazione = FormValutazione()

    if request.method == 'POST' and request.user.is_authenticated:

        if 'invia_commento' in request.POST:
            form_commento = FormCommento(request.POST)
            if form_commento.is_valid():
                c = form_commento.save(commit=False)
                c.utente   = request.user
                c.percorso = percorso
                c.save()
                messages.success(request, 'Commento pubblicato.')
                return redirect('dettaglio_percorso', id=id)

        elif 'invia_valutazione' in request.POST:
            esistente = Valutazione.objects.filter(utente=request.user, percorso=percorso).first()
            form_valutazione = FormValutazione(request.POST, instance=esistente)
            if form_valutazione.is_valid():
                v = form_valutazione.save(commit=False)
                v.utente   = request.user
                v.percorso = percorso
                v.save()
                messages.success(request, 'Valutazione salvata.')
                return redirect('dettaglio_percorso', id=id)

    return render(request, 'generale/dettaglio_percorso.html', {
        'percorso':         percorso,
        'commenti':         commenti,
        'media_voto':       media_voto,
        'media_voto_int':   round(media_voto) if media_voto else 0,
        'voto_utente':      voto_utente,
        'form_commento':    form_commento,
        'form_valutazione': form_valutazione,
    })


# ── ELIMINA COMMENTO ──────────────────────────────────────────────────────────

@login_required
def elimina_commento(request, id):
    commento = get_object_or_404(Commento, id=id, utente=request.user)
    if commento.falesia:
        dest = redirect('dettaglio_falesia', id=commento.falesia.id)
    else:
        dest = redirect('dettaglio_percorso', id=commento.percorso.id)
    commento.delete()
    messages.success(request, 'Commento eliminato.')
    return dest


# ── AUTENTICAZIONE ────────────────────────────────────────────────────────────

def vista_login(request):
    if request.user.is_authenticated:
        return redirect('home')
    if request.method == 'POST':
        form = AuthenticationForm(data=request.POST)
        if form.is_valid():
            login(request, form.get_user())
            return redirect(request.GET.get('next', 'home'))
    else:
        form = AuthenticationForm()
    return render(request, 'generale/login.html', {'form': form})


def vista_logout(request):
    if request.method == 'POST':
        logout(request)
    return redirect('home')


def vista_registrazione(request):
    if request.user.is_authenticated:
        return redirect('home')
    if request.method == 'POST':
        form = FormRegistrazione(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, f'Benvenuto, {user.username}!')
            return redirect('home')
    else:
        form = FormRegistrazione()
    return render(request, 'generale/registrazione.html', {'form': form})


# ── PROFILO ───────────────────────────────────────────────────────────────────

@login_required
def vista_profilo(request):
    profilo = request.user.profilo

    # Inizializziamo tutti e tre i form vuoti (per il GET)
    form_img      = FormProfiloImmagine(instance=profilo)
    form_dati     = FormDatiUtente(instance=request.user)
    form_password = FormCambioPassword(user=request.user)

    if request.method == 'POST':

        # Il campo 'azione' nell'HTML ci dice quale form è stato inviato,
        # così possiamo gestirli separatamente nella stessa view.

        if 'salva_immagine' in request.POST:
            form_img = FormProfiloImmagine(request.POST, request.FILES, instance=profilo)
            if form_img.is_valid():
                form_img.save()
                messages.success(request, 'Immagine profilo aggiornata.')
                return redirect('profilo')

        elif 'salva_username' in request.POST:
            nuovo_username = request.POST.get('username', '').strip()
            if nuovo_username:
                if User.objects.filter(username=nuovo_username).exclude(pk=request.user.pk).exists():
                    messages.error(request, 'Username già in uso.')
                else:
                    request.user.username = nuovo_username
                    request.user.save()
                    messages.success(request, 'Username aggiornato.')
            return redirect('profilo')

        elif 'salva_email' in request.POST:
            nuova_email = request.POST.get('email', '').strip()
            if nuova_email:
                request.user.email = nuova_email
                request.user.save()
                messages.success(request, 'Email aggiornata.')
            return redirect('profilo')

        elif 'salva_password' in request.POST:
            form_password = FormCambioPassword(user=request.user, data=request.POST)
            if form_password.is_valid():
                form_password.salva()
                # Dopo aver cambiato la password Django invalida la sessione,
                # quindi bisogna ri-autenticare l'utente per non farlo sloggare.
                from django.contrib.auth import update_session_auth_hash
                update_session_auth_hash(request, request.user)
                messages.success(request, 'Password aggiornata.')
                return redirect('profilo')

    commenti_utente = Commento.objects.filter(utente=request.user).order_by('-data')
    return render(request, 'generale/profilo.html', {
        'form_img':        form_img,
        'form_dati':       form_dati,
        'form_password':   form_password,
        'commenti_utente': commenti_utente,
    })