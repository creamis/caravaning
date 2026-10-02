from django.urls import path
from . import views

app_name = 'users'

urlpatterns = [
    path('viajero/<str:username>/', views.public_profile, name='public_profile'),

    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('register/', views.register, name='register'),
    path('profile/', views.profile, name='profile'),
    path('profile/edit/', views.profile_edit, name='profile_edit'), 
]


