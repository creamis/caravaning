from django.urls import path
from . import views

app_name = 'experiences'

urlpatterns = [
    path('', views.home, name='home'),
]
