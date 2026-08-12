from django.db import migrations


def fix_water_image(apps, schema_editor):
    Post = apps.get_model("blog", "Post")
    PostImage = apps.get_model("blog", "PostImage")

    post = Post.objects.filter(slug="agua-caravana-depositos-bombas-bidones-accesorios").first()
    if not post:
        return

    # Imagen de producto real del Whale Watermaster EP1642.
    # Se utiliza una URL directa de una tienda especializada que publica la fotografía del producto.
    image_url = "https://outboardpartsonline.co.uk/cdn/shop/files/EP1642-main.jpg?v=1738147219"

    PostImage.objects.filter(post=post).delete()
    PostImage.objects.create(post=post, image_url=image_url)


def reverse_fix(apps, schema_editor):
    pass


class Migration(migrations.Migration):
    dependencies = [("blog", "0026_imagenes_productos_coincidentes")]
    operations = [migrations.RunPython(fix_water_image, reverse_fix)]
