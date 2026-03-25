from django.db import models

# Create your models here.
from django.db import models
from django.contrib.auth.models import User
from apps.falesie.models import Falesia, Percorso

class Commento(models.Model):
    utente = models.ForeignKey(User, on_delete=models.CASCADE)
    falesia = models.ForeignKey(Falesia, on_delete=models.CASCADE, null=True, blank=True)
    percorso = models.ForeignKey(Percorso, on_delete=models.CASCADE, null=True, blank=True)
    testo = models.TextField()
    data = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.utente.username} - {self.data:%d/%m/%Y}"


class Valutazione(models.Model):
    VOTO_CHOICES = [
        (1, '1'),
        (2, '2'),
        (3, '3'),
        (4, '4'),
        (5, '5'),
    ]
    utente = models.ForeignKey(User, on_delete=models.CASCADE)
    falesia = models.ForeignKey(Falesia, on_delete=models.CASCADE, null=True, blank=True)
    percorso = models.ForeignKey(Percorso, on_delete=models.CASCADE, null=True, blank=True)
    voto = models.IntegerField(choices=VOTO_CHOICES)

class Preferito(models.Model):
    utente = models.ForeignKey(User, on_delete=models.CASCADE)
    falesia = models.ForeignKey(Falesia, on_delete=models.CASCADE, null=True, blank=True)
    percorso = models.ForeignKey(Percorso, on_delete=models.CASCADE, null=True, blank=True)