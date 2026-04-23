from django.urls import path
from . import views


app_name = 'pages'

urlpatterns = [
    path('sobre-nosotros/', views.AboutView.as_view(), name='about'),
    path('contacto/', views.ContactView.as_view(), name='contact'),
    path('aviso-legal/', views.LegalView.as_view(), name='legal'),
    path('privacidad/', views.PrivacyView.as_view(), name='privacy'),
    path('cookies/', views.CookiesView.as_view(), name='cookies'),
    path('afiliados/', views.AffiliatesView.as_view(), name='affiliates'),
]
