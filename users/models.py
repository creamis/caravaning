# users/models.py
from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver

class Profile(models.Model):
    # Relación uno a uno con el modelo de Usuario de Django
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    bio = models.TextField(blank=True, null=True, verbose_name="Biografía")
    profile_picture = models.ImageField(upload_to='profile_pics/', default='profile_pics/default.jpg', verbose_name="Foto de perfil")
    phone_number = models.CharField(max_length=20, blank=True, null=True, verbose_name="Número de teléfono")

    def __str__(self):
        return f'Perfil de {self.user.username}'

@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)
