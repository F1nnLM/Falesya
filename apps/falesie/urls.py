from django.urls import path
from .views import FalesiaListView, FalesiaDetailView

app_name = 'falesie'

urlpatterns = [
    path('', FalesiaListView.as_view(), name='home'),
    path('falesia/<int:pk>/', FalesiaDetailView.as_view(), name='dettaglio'),
]