from django.shortcuts import render
from django.views.generic import ListView, DetailView
from .models import Falesia

# Vista per la Home Page (Lista falesie con ricerca)
class FalesiaListView(ListView):
    model = Falesia
    template_name = 'falesie/home.html'
    context_object_name = 'falesie'

    def get_queryset(self):
        query = self.request.GET.get('q')
        if query:
            return Falesia.objects.filter(nome__icontains=query) | Falesia.objects.filter(comune__icontains=query)
        return Falesia.objects.all()

# Vista per il Dettaglio Falesia
class FalesiaDetailView(DetailView):
    model = Falesia
    template_name = 'falesie/dettaglio.html'
    context_object_name = 'falesia'