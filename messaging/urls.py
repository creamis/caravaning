from django.urls import path
from . import views

app_name = 'messaging'

urlpatterns = [
    path('contactar/<int:pk>/', views.contact_seller, name='contact_seller'),
]