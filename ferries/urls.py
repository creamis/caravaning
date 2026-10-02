from django.urls import path
from . import views

app_name = 'ferries'

urlpatterns = [
    path('', views.home, name='home'),
]
