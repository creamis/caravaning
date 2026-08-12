from django.db import migrations

POST_SLUG = "20-accesorios-imprescindibles-camper-menos-50-euros"

PRODUCTS = []


def add_camper_products(apps, schema_editor):
    Post = apps.get_model("blog", "Post")
    User = apps.get_model("auth", "User")

    author = User.objects.filter(username="miguel").first() or User.objects.filter(is_superuser=True).first()
    if not author:
        return

    post = Post.objects.filter(slug=POST_SLUG).first()
    if post is None:
        post = Post.objects.create(
            author=author,
            title="Los 20 accesorios imprescindibles para una camper por menos de 50 €",
            slug=POST_SLUG,
            meta_description="Descubre 20 accesorios imprescindibles para camper por menos de 50 €. Organización, cocina, iluminación, energía y comodidad para viajar mejor sin gastar una fortuna.",
            content="<p>Estamos preparando una guía con 20 accesorios camper económicos y prácticos.</p>",
            status="PUBLISHED",
        )
    else:
        if not post.author_id:
            post.author = author
            post.save(update_fields=["author"])


def remove_camper_products(apps, schema_editor):
    pass


class Migration(migrations.Migration):
    dependencies = [("blog", "0013_fix_frescos_verano_images")]
    operations = [migrations.RunPython(add_camper_products, remove_camper_products)]
