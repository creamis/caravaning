# listings/models.py
from django.db import models
from django.contrib.auth.models import User
from django.urls import reverse

class Listing(models.Model):
    class ListingType(models.TextChoices):
        SALE = 'SALE', 'Venta'

    class Category(models.TextChoices):
        CARAVANA = 'CARAVANA', 'Caravana'
        AUTOCARAVANA = 'AUTOCARAVANA', 'Autocaravana'
        CAMPER = 'CAMPER', 'Camper'

    # Nuevas clases para choices
    class FuelType(models.TextChoices):
        DIESEL = 'DIESEL', 'Diésel'
        GASOLINE = 'GASOLINE', 'Gasolina'
        ELECTRIC = 'ELECTRIC', 'Eléctrico'
        HYBRID = 'HYBRID', 'Híbrido'
        LPG = 'LPG', 'GLP'
        OTHER = 'OTHER', 'Otro'

    class TransmissionType(models.TextChoices):
        MANUAL = 'MANUAL', 'Manual'
        AUTOMATIC = 'AUTOMATIC', 'Automática'

    class SellerType(models.TextChoices):
        PRIVATE = 'PRIVATE', 'Particular'
        PROFESSIONAL = 'PROFESSIONAL', 'Profesional'

    owner = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name="Propietario")
    seller_type = models.CharField(max_length=15, choices=SellerType.choices, default=SellerType.PRIVATE, verbose_name="Tipo de vendedor")
    title = models.CharField(max_length=200, verbose_name="Título")
    description = models.TextField(verbose_name="Descripción")
    price = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="Precio (€)")
    listing_type = models.CharField(max_length=10, choices=ListingType.choices, default=ListingType.SALE, verbose_name="Tipo de anuncio")
    category = models.CharField(max_length=20, choices=Category.choices, default=Category.CARAVANA, verbose_name="Categoría")
    location = models.CharField(max_length=100, verbose_name="Ubicación")
    is_available = models.BooleanField(default=True, verbose_name="Disponible")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    # --- Nuevas características del vehículo ---
    year = models.PositiveIntegerField(null=True, blank=True, verbose_name="Año de fabricación")
    seats = models.PositiveIntegerField(null=True, blank=True, verbose_name="Plazas para viajar")
    berths = models.PositiveIntegerField(null=True, blank=True, verbose_name="Plazas para dormir")
    mileage = models.PositiveIntegerField(null=True, blank=True, verbose_name="Kilometraje (km)")
    fuel_type = models.CharField(max_length=10, choices=FuelType.choices, null=True, blank=True, verbose_name="Combustible")
    transmission = models.CharField(max_length=10, choices=TransmissionType.choices, null=True, blank=True, verbose_name="Transmisión")
    length = models.DecimalField(max_digits=4, decimal_places=2, null=True, blank=True, verbose_name="Longitud (m)")
    weight = models.PositiveIntegerField(null=True, blank=True, verbose_name="Peso (MMA en kg)")
    has_bathroom = models.BooleanField(default=False, verbose_name="Baño con WC")
    has_shower = models.BooleanField(default=False, verbose_name="Ducha")
    has_kitchen = models.BooleanField(default=False, verbose_name="Cocina")
    has_heating = models.BooleanField(default=False, verbose_name="Calefacción")
    has_air_conditioning = models.BooleanField(default=False, verbose_name="Aire acondicionado")
    pets_allowed = models.BooleanField(default=False, verbose_name="Admite mascotas")
    has_solar_panels = models.BooleanField(default=False, verbose_name="Placas solares")

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('listings:listing_detail', kwargs={'pk': self.pk})

# Opcional pero recomendado: un modelo para gestionar múltiples fotos por anuncio
class ListingImage(models.Model):
    listing = models.ForeignKey(Listing, related_name='images', on_delete=models.CASCADE)
    image = models.ImageField(upload_to='listing_images/')

    def __str__(self):
        return f"Imagen para {self.listing.title}"


# Añade esto a d:\Miguel\django\caravaning-django\listings\models.py

class Review(models.Model):
    listing = models.ForeignKey(Listing, on_delete=models.CASCADE, related_name='reviews')
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name='listing_reviews')
    content = models.TextField(verbose_name="Opinión")
    rating = models.PositiveSmallIntegerField(default=5, verbose_name="Calificación")
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f"Reseña de {self.author.username} para {self.listing.title}"
