from django.db import models
from django.contrib.auth.models import User
from django.urls import reverse

class Destination(models.Model):
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name='destinations')
    title = models.CharField(max_length=200, verbose_name="Nombre del lugar")
    description = models.TextField(verbose_name="¿Por qué es genial este lugar?")
    location = models.CharField(max_length=255, verbose_name="Ubicación", help_text="Ej: Cabo de Gata, Almería o una dirección específica")
    image = models.ImageField(upload_to='destinations/', verbose_name="Foto de portada")
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('destinations:destination_detail', kwargs={'pk': self.pk})

class DestinationImage(models.Model):
    destination = models.ForeignKey(Destination, related_name='images', on_delete=models.CASCADE)
    image = models.ImageField(upload_to='destinations/gallery/')

    def __str__(self):
        return f"Imagen para {self.destination.title}"

class DestinationReview(models.Model):
    destination = models.ForeignKey(Destination, on_delete=models.CASCADE, related_name='reviews')
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    rating = models.PositiveSmallIntegerField(default=5, verbose_name="Valoración")
    content = models.TextField(verbose_name="Comentario")
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f"Reseña de {self.author.username} en {self.destination.title}"