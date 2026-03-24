from django.db import models

# Create your models here.
from django.db import models

class Falesia(models.Model):
    nome = models.CharField(max_length=200)
    tipo_roccia = models.CharField(max_length=100)
    latitudine = models.DecimalField(max_digits=9, decimal_places=6)
    longitudine = models.DecimalField(max_digits=9, decimal_places=6)
    comune = models.CharField(max_length=100)
    provincia = models.CharField(max_length=100)
    regione = models.CharField(max_length=100)
    paese = models.CharField(max_length=100)
    descrizione = models.TextField()
    esposizione = models.CharField(max_length=50)
    stagione_consigliata = models.CharField(max_length=50)
    immagine = models.ImageField(upload_to='falesie/', blank=True)

    def __str__(self):
        return self.nome


class Percorso(models.Model):
    TIPO_CHOICES = [
        ('sport', 'Sportiva'),
        ('boulder', 'Boulder'),
        ('trad', 'Tradizionale'),
    ]
    nome = models.CharField(max_length=200)
    grado = models.CharField(max_length=10)
    n_soste = models.IntegerField()
    tipo = models.CharField(max_length=20, choices=TIPO_CHOICES)
    altezza = models.IntegerField()
    n_spittature = models.IntegerField()
    distanza_spit = models.DecimalField(max_digits=5, decimal_places=2)
    descrizione = models.TextField()
    immagine = models.ImageField(upload_to='percorsi/', blank=True)
    falesia = models.ForeignKey(Falesia, on_delete=models.CASCADE, related_name='percorsi')

    def __str__(self):
        return self.nome