from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import Commento, Valutazione, Profilo


# ── AUTENTICAZIONE ────────────────────────────────────────────────────────────

class FormRegistrazione(UserCreationForm):
    """
    Estende UserCreationForm (già incluso in Django) aggiungendo il campo email.
    UserCreationForm gestisce già username, password1, password2 con validazione.
    """
    email = forms.EmailField(required=True, label="Email")

    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']

    def save(self, commit=True):
        user = super().save(commit=False)
        user.email = self.cleaned_data['email']
        if commit:
            user.save()
            # Il signal post_save in models.py crea automaticamente il Profilo
        return user


# ── PROFILO ───────────────────────────────────────────────────────────────────

class FormProfiloImmagine(forms.ModelForm):
    """Form per aggiornare solo l'immagine del profilo."""
    class Meta:
        model = Profilo
        fields = ['immagine_profilo']


# ── COMMENTO ──────────────────────────────────────────────────────────────────

class FormCommento(forms.ModelForm):
    """
    Form semplice per scrivere un commento.
    Il testo viene limitato a 1000 caratteri nel widget.
    utente, falesia/percorso vengono assegnati nella view, non dall'utente.
    """
    class Meta:
        model = Commento
        fields = ['testo']
        widgets = {
            'testo': forms.Textarea(attrs={
                'rows': 3,
                'placeholder': 'Scrivi un commento...',
                'maxlength': 1000,
            })
        }
        labels = {'testo': ''}


# ── VALUTAZIONE ───────────────────────────────────────────────────────────────

class FormValutazione(forms.ModelForm):
    """
    Form per votare da 1 a 5 stelle.
    Usa radio button invece di select per una UX migliore.
    """
    class Meta:
        model = Valutazione
        fields = ['voto']
        widgets = {
            'voto': forms.RadioSelect()
        }
        labels = {'voto': 'La tua valutazione'}
