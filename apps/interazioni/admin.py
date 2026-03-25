from django.contrib import admin
from .models import Commento, Preferito, Valutazione

# Register your models here.
admin.site.register(Commento)
admin.site.register(Preferito)
admin.site.register(Valutazione)