import html
from django.db import models
from django.contrib.auth.models import User
from django.urls import reverse
from django.utils.html import strip_tags
from ckeditor.fields import RichTextField

class Destination(models.Model):
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name='destinations')
    title = models.CharField(max_length=200, verbose_name="Nombre del lugar")
    description = RichTextField(verbose_name="¿Por qué es genial este lugar?")
    location = models.CharField(max_length=255, verbose_name="Ubicación", help_text="Ej: Cabo de Gata, Almería o una dirección específica")
    image = models.ImageField(upload_to='destinations/', verbose_name="Foto de portada", null=True, blank=True)
    image_url = models.URLField(max_length=500, blank=True, null=True, verbose_name="URL de imagen externa")
    created_at = models.DateTimeField(auto_now_add=True)

    def get_image_url(self):
        """Retorna la URL de la imagen de portada, priorizando la subida local."""
        if self.image:
            return self.image.url
        return self.image_url

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('destinations:destination_detail', kwargs={'pk': self.pk})

    @property
    def plain_description(self):
        """Retorna la descripción sin etiquetas HTML, ideal para listados."""
        text = strip_tags(html.unescape(self.description))
        return html.unescape(text).replace('\xa0', ' ').strip()

class DestinationImage(models.Model):
    destination = models.ForeignKey(Destination, related_name='images', on_delete=models.CASCADE)
    image = models.ImageField(upload_to='destinations/gallery/', null=True, blank=True)
    image_url = models.URLField(max_length=500, blank=True, null=True, verbose_name="URL de imagen externa")

    def get_url(self):
        """Retorna la URL de la imagen de galería, priorizando la subida local."""
        if self.image:
            return self.image.url
        return self.image_url

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