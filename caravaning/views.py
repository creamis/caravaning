from django.shortcuts import render
from django.db.models import Avg
from listings.models import Listing
from destinations.models import Destination # Importamos el modelo Destination
from django.contrib.auth.models import User
from caravaning.trip_engine import get_suggested_trip
from django.db.models import Q
from django.urls import reverse
from blog.models import Post

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
        'destinations_count': destinations_count,
        'users_count': users_count,
        'average_rating': round(avg_rating, 1),
        'suggested_trip': get_suggested_trip(),
    }
    return render(request, 'home.html', context)

def search(request):
    """
    Buscador global de Caravaning Project.
    Busca en destinos, artículos publicados y secciones principales.
    No modifica ningún modelo ni necesita migraciones.
    """
    query = request.GET.get("q", "").strip()

    destinations = Destination.objects.none()
    posts = Post.objects.none()
    sections = []

    if query:
        destinations = Destination.objects.filter(
            Q(title__icontains=query) |
            Q(location__icontains=query) |
            Q(description__icontains=query)
        ).distinct()[:12]

        posts = Post.objects.filter(
            Q(title__icontains=query) |
            Q(meta_description__icontains=query) |
            Q(content__icontains=query),
            status=Post.Status.PUBLISHED
        ).distinct()[:12]

        # --------------------------------------------------
        # Secciones estáticas
        # --------------------------------------------------
        q = query.casefold()

        section_rules = [
            {
                "title": "Destinos",
                "description": "Lugares y rutas para tu próxima escapada.",
                "icon": "bi-geo-alt-fill",
                "url": reverse("destinations:destination_list"),
                "keywords": [
                    "destino", "destinos", "ruta", "rutas",
                    "viaje", "viajar", "escapada", "lugares"
                ],
            },
            {
                "title": "Experiencias",
                "description": "Actividades y planes para completar el viaje.",
                "icon": "bi-compass",
                "url": reverse("experiences:home"),
                "keywords": [
                    "experiencia", "experiencias", "actividad",
                    "actividades", "excursion", "excursión",
                    "aventura", "que hacer", "qué hacer"
                ],
            },
            {
                "title": "Campings",
                "description": "Campings, parcelas y opciones para hacer noche.",
                "icon": "bi-tree",
                "url": reverse("camping"),
                "keywords": [
                    "camping", "campings", "parcela", "parcelas",
                    "bungalow", "bungalows", "dormir", "pernoctar"
                ],
            },
            {
                "title": "AlohaCamp",
                "description": "Cabañas, glamping y alojamientos en la naturaleza.",
                "icon": "bi-house-heart",
                "url": reverse("alohacamp"),
                "keywords": [
                    "alohacamp", "glamping", "cabaña", "cabañas",
                    "alojamiento", "alojamientos"
                ],
            },
            {
                "title": "Alquiler de campers y autocaravanas",
                "description": "Opciones de alquiler para empezar tu ruta.",
                "icon": "bi-key-fill",
                "url": reverse("listings:external_rentals"),
                "keywords": [
                    "alquiler", "alquilar", "rentar",
                    "camperdays", "alquiler camper",
                    "alquiler autocaravana"
                ],
            },
            {
                "title": "Ferries",
                "description": "Rutas para cruzar el mar con tu vehículo.",
                "icon": "bi-water",
                "url": reverse("ferries:home"),
                "keywords": [
                    "ferry", "ferries", "barco", "barcos",
                    "baleares", "mallorca", "menorca", "ibiza",
                    "cerdeña", "sicilia", "corcega", "córcega",
                    "marruecos", "ceuta", "melilla", "canarias"
                ],
            },
            {
                "title": "Blog",
                "description": "Guías, consejos y contenidos sobre caravaning.",
                "icon": "bi-journal-text",
                "url": reverse("blog:post_list"),
                "keywords": [
                    "blog", "guia", "guía", "guias", "guías",
                    "consejo", "consejos", "articulo", "artículo"
                ],
            },
            {
                "title": "Tienda y accesorios",
                "description": "Accesorios y equipamiento para viajar.",
                "icon": "bi-bag",
                "url": reverse("shop:product_list"),
                "keywords": [
                    "tienda", "accesorio", "accesorios",
                    "equipamiento", "producto", "productos",
                    "amazon"
                ],
            },
            {
                "title": "Vehículos en venta",
                "description": "Campers, caravanas y autocaravanas anunciadas.",
                "icon": "bi-tag",
                "url": reverse("listings:listing_list") + "?listing_type=SALE",
                "keywords": [
                    "comprar", "compra", "venta", "vender",
                    "vehiculo", "vehículo", "vehiculos", "vehículos",
                    "caravana", "caravanas", "autocaravana",
                    "autocaravanas", "camper", "campers"
                ],
            },
        ]

        for section in section_rules:
            if any(keyword in q for keyword in section["keywords"]):
                sections.append({
                    key: value
                    for key, value in section.items()
                    if key != "keywords"
                })

    context = {
        "query": query,
        "search_destinations": destinations,
        "search_posts": posts,
        "search_sections": sections,
    }

    return render(request, "search_results.html", context)
