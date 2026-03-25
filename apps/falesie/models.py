from django.db import models

# Create your models here.
from django.db import models

class Falesia(models.Model):
    ROCK_TYPE_CHOICES = [
    ("limestone", "Calcare"),
    ("granite", "Granito"),
    ("sandstone", "Arenaria"),
    ("basalt", "Basalto"),
    ("conglomerate", "Conglomerato"),
    ("schist", "Scisto"),
    ("gneiss", "Gneiss"),
    ("quartzite", "Quarzite"),
    ("dolomite", "Dolomia"),
    ("tuff", "Tufo"),
    ("rhyolite", "Riolite"),
    ("gabbro", "Gabbro"),
    ("slate", "Ardesia"),
    ("marble", "Marmo"),
    ("volcanic", "Vulcanico"),
]
    
    STAGIONI = [
        ("primavera", "Primavera"),
        ("estate", "Estate"),
        ("autunno", "Autunno"),
        ("inverno", "Inverno"),
    ]

    ESPOSIZIONE = [
        ("nord", "Nord"),
        ("nord-est", "Nord-Est"),
        ("est", "Est"),
        ("sud-est", "Sud-Est"),
        ("sud", "Sud"),
        ("sud-ovest", "Sud-Ovest"),
        ("ovest", "Ovest"),
        ("nord-ovest", "Nord-Ovest"),
    ]
    
    nome = models.CharField(max_length=200)
    tipo_roccia = models.CharField(max_length=100, choices=ROCK_TYPE_CHOICES)
    latitudine = models.DecimalField(max_digits=9, decimal_places=6)
    longitudine = models.DecimalField(max_digits=9, decimal_places=6)
    comune = models.CharField(max_length=100)
    provincia = models.CharField(max_length=100)
    regione = models.CharField(max_length=100)
    paese = models.CharField(max_length=100)
    descrizione = models.TextField()
    esposizione = models.CharField(max_length=50, choices=ESPOSIZIONE)
    stagione_consigliata = models.CharField(max_length=50, choices=STAGIONI)
    immagine = models.ImageField(upload_to='falesie/', blank=True)

    def __str__(self):
        return self.nome


class Percorso(models.Model):
    TIPO_CHOICES = [
        ('sport', 'Sportiva'),
        ('boulder', 'Boulder'),
        ('trad', 'Tradizionale'),
    ]

    SCALA_FRANCESE_GRADI = [
        ('1', '1'),
        ('2', '2'),
        ('3', '3'),
        ('4a', '4a'),
        ('4b', '4b'),
        ('4c', '4c'),
        ('5a', '5a'),
        ('5b', '5b'),
        ('5c', '5c'),
        ('6a', '6a'),
        ('6a+', '6a+'),
        ('6b', '6b'),
        ('6b+', '6b+'),
        ('6c', '6c'),
        ('6c+', '6c+'),
        ('7a', '7a'),
        ('7a+', '7a+'),
        ('7b', '7b'),
        ('7b+', '7b+'),
        ('7c', '7c'),
        ('7c+', '7c+'),
        ('8a', '8a'),
        ('8a+', '8a+'),
        ('8b', '8b'),
        ('8b+', '8b+'),
        ('8c', '8c'),
        ('8c+', '8c+'),
    ]
    nome = models.CharField(max_length=200)
    grado = models.CharField(max_length=10, choices=SCALA_FRANCESE_GRADI)
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