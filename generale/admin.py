from django.contrib import admin
from .models import Commento, Preferito, Valutazione, Falesia, Percorso
# Register your models here.
admin.site.register(Falesia)
admin.site.register(Percorso)
admin.site.register(Commento)
admin.site.register(Preferito)
admin.site.register(Valutazione)

