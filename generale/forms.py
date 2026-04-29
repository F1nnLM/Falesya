from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import Commento, Valutazione, Profilo


#autenticazione


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
            #Il signal post_save in models.py crea automaticamente il Profilo
        return user


#profilo

class FormProfiloImmagine(forms.ModelForm):
    """Form per aggiornare solo l'immagine del profilo"""
    class Meta:
        model = Profilo
        fields = ['immagine_profilo']


#modifica dati utente

class FormDatiUtente(forms.ModelForm):
    """
    Permette di modificare username ed email dell'utente.
    Usa il modello User direttamente — nessun campo extra necessario
    """
    class Meta:
        model = User
        fields = ['username', 'email']
        labels = {
            'username': 'Username',
            'email': 'Email',
        }


class FormCambioPassword(forms.Form):
    """
    Form manuale (non ModelForm) per il cambio password.
    Non usiamo PasswordChangeForm di Django perché vogliamo
    controllare il layout noi stessi, ma la logica è identica:
    verifica la password attuale, chiede la nuova due volte.
    """
    password_attuale  = forms.CharField(widget=forms.PasswordInput, label='Password attuale')
    nuova_password    = forms.CharField(widget=forms.PasswordInput, label='Nuova password')
    conferma_password = forms.CharField(widget=forms.PasswordInput, label='Conferma nuova password')

    def __init__(self, user, *args, **kwargs):
        #Riceviamo l'utente per poter verificare la password attuale
        self.user = user
        super().__init__(*args, **kwargs)

    def clean(self):
        """
        clean() viene chiamato da is_valid() dopo che i singoli campi
        sono stati validati. validazioni che coinvolgono
        più campi contemporaneamente.
        """
        cleaned = super().clean()
        attuale   = cleaned.get('password_attuale')
        nuova     = cleaned.get('nuova_password')
        conferma  = cleaned.get('conferma_password')

        #Verifica che la password attuale sia corretta
        if attuale and not self.user.check_password(attuale):
            raise forms.ValidationError({'password_attuale': 'Password attuale non corretta.'})

        #Verifica che nuova e conferma coincidano
        if nuova and conferma and nuova != conferma:
            raise forms.ValidationError({'conferma_password': 'Le password non coincidono.'})

        return cleaned

    def salva(self):
        """Imposta la nuova password e salva. Va chiamato dopo is_valid()."""
        self.user.set_password(self.cleaned_data['nuova_password'])
        self.user.save()


#commento

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


#valutazione

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

