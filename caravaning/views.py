from django.shortcuts import render
from django.db.models import Avg
from listings.models import Listing
from destinations.models import Destination # Importamos el modelo Destination
from django.contrib.auth.models import User

def index(request):
    # Contamos solo los anuncios que están marcados como disponibles
    active_listings_count = Listing.objects.filter(is_available=True).count()
    # Contamos todos los destinos publicados
    destinations_count = Destination.objects.count()
    # Contamos el total de usuarios registrados
    users_count = User.objects.count()
    # Calculamos la valoración media real de todos los anuncios
    avg_rating = Listing.objects.aggregate(Avg('reviews__rating'))['reviews__rating__avg'] or 0
    
    context = {
        'active_listings_count': active_listings_count,
        'destinations_count': destinations_count, # Añadimos el conteo de destinos al contexto
        'users_count': users_count,
        'average_rating': round(avg_rating, 1),
    }
    return render(request, 'home.html', context)