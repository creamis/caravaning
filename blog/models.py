# blog/models.py
from django.db import models
from django.urls import reverse
from django.contrib.auth.models import User
from django.utils.text import slugify
from ckeditor.fields import RichTextField

class Post(models.Model):
    class Status(models.TextChoices):
        DRAFT = 'DRAFT', 'Borrador'
        PUBLISHED = 'PUBLISHED', 'Publicado'

    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name='blog_posts', verbose_name="Autor")
    title = models.CharField(max_length=250, verbose_name="Título")
    slug = models.SlugField(max_length=250, unique=True, help_text="URL amigable, se genera automáticamente")
    content = RichTextField(verbose_name="Contenido")
    status = models.CharField(max_length=10, choices=Status.choices, default=Status.DRAFT, blank=True, verbose_name="Estado")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def save(self, *args, **kwargs):
        if not self.slug:
            base_slug = slugify(self.title)
            unique_slug = base_slug
            num = 1
            # Comprueba si ya existe un post con este slug.
            # Si es una actualización, excluye la instancia actual de la comprobación.
            while Post.objects.filter(slug=unique_slug).exclude(pk=self.pk).exists():
                unique_slug = f"{base_slug}-{num}"
                num += 1
            self.slug = unique_slug
        super().save(*args, **kwargs)

    def get_absolute_url(self):
        return reverse('blog:post_detail', kwargs={'slug': self.slug})

    @property
    def reading_time(self):
        # Estimación: 200 palabras por minuto
        word_count = len(self.content.split())
        return max(1, round(word_count / 200))

    def __str__(self):
        return self.title

class PostImage(models.Model):
    """Modelo para almacenar las imágenes de un post."""
    post = models.ForeignKey(Post, related_name='images', on_delete=models.CASCADE)
    image = models.ImageField(upload_to='blog_images/', verbose_name="Imagen")

    def __str__(self):
        return f"Imagen para el post: {self.post.title}"

class Comment(models.Model):
    """Modelo para almacenar los comentarios de un post."""
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='comments', verbose_name="Post")
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name='blog_comments', verbose_name="Autor")
    content = models.TextField(verbose_name="Contenido del comentario")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Fecha de creación")

    class Meta:
        ordering = ['created_at']

    def __str__(self):
        return f'Comentario de {self.author.username} en "{self.post.title}"'
