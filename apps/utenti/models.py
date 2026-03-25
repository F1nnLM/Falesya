from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver

class Profilo(models.Model):
    utente = models.OneToOneField(User, on_delete=models.CASCADE)
    immagine_profilo = models.ImageField(upload_to='profili/', blank=True, null=True)

    def __str__(self):
        return self.utente.username

@receiver(post_save, sender=User)
def crea_profilo(sender, instance, created, **kwargs):
    if created:
        Profilo.objects.create(utente=instance)


@receiver(post_save, sender=User)
def salva_profilo(sender, instance, **kwargs):
    instance.profilo.save()