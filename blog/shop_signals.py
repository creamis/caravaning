from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import Post
from .shop_sync import sync_post_products


@receiver(
    post_save,
    sender=Post,
    dispatch_uid="blog_sync_products_to_shop",
)
def synchronize_shop(sender, instance, **kwargs):
    sync_post_products(instance)
