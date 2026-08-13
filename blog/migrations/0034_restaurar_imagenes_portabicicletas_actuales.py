from django.db import migrations
import re

POST_SLUG = "portabicicletas-camper-autocaravana"

# Fotografías reales y recientes del producto/modelo. Se utilizan únicamente
# como imágenes ilustrativas del producto mencionado en cada apartado.
FIAMMA_IMAGE = "https://www.masquecamper.com/wp-content/uploads/2025/04/Carry-Bike-Pro-C-Deep-Black-FIAMMA-02096-10A-7.jpg"
THULE_IMAGE = "https://kombilife.com.au/cdn/shop/files/IMG-5995_525x700.jpg?v=1771392306"


def product_image_html(url, alt):
    return (
        f'<img src="{url}" alt="{alt}" loading="lazy" '
        'style="display:block;width:100%;max-width:100%;aspect-ratio:16/9;'
        'height:auto;object-fit:contain;border-radius:16px;margin:18px 0;">'
    )


def restore_product_images(html):
    headings = [
        (
            "1. Fiamma Carry-Bike para autocaravana y camper",
            FIAMMA_IMAGE,
            "Fiamma Carry-Bike Pro C Deep Black para autocaravana y camper",
        ),
        (
            "2. Thule Elite Van XT",
            THULE_IMAGE,
            "Thule Elite Van XT instalado en una furgoneta camper",
        ),
    ]

    for heading, image_url, alt in headings:
        pattern = rf"(<h2>\s*{re.escape(heading)}\s*</h2>)(.*?)(?=<h2>|\Z)"

        def repl(match, image_url=image_url, alt=alt):
            section = match.group(2)
            # Evita duplicados si la migración se ejecuta sobre contenido ya corregido.
            section = re.sub(r"<img\b[^>]*>", "", section, flags=re.IGNORECASE)
            image = product_image_html(image_url, alt)
            if "</p>" in section.lower():
                return match.group(1) + section.replace("</p>", f"</p>{image}", 1)
            return match.group(1) + image + section

        html = re.sub(pattern, repl, html, flags=re.IGNORECASE | re.DOTALL)

    return html


def restore_images(apps, schema_editor):
    Post = apps.get_model("blog", "Post")
    PostImage = apps.get_model("blog", "PostImage")

    post = Post.objects.filter(slug=POST_SLUG).first()
    if not post:
        return

    # Restauramos únicamente las dos imágenes actuales en el carrusel de cabecera.
    PostImage.objects.filter(post=post).delete()
    PostImage.objects.create(post=post, image_url=FIAMMA_IMAGE)
    PostImage.objects.create(post=post, image_url=THULE_IMAGE)

    # Y restauramos una imagen específica dentro de cada apartado del artículo.
    post.content = restore_product_images(post.content or "")
    post.save(update_fields=["content"])


def remove_images(apps, schema_editor):
    Post = apps.get_model("blog", "Post")
    PostImage = apps.get_model("blog", "PostImage")

    post = Post.objects.filter(slug=POST_SLUG).first()
    if not post:
        return

    PostImage.objects.filter(post=post).delete()

    def remove_from_sections(html):
        for heading in [
            "1. Fiamma Carry-Bike para autocaravana y camper",
            "2. Thule Elite Van XT",
        ]:
            pattern = rf"(<h2>\s*{re.escape(heading)}\s*</h2>)(.*?)(?=<h2>|\Z)"
            html = re.sub(
                pattern,
                lambda m: m.group(1) + re.sub(r"<img\b[^>]*>", "", m.group(2), flags=re.IGNORECASE),
                html,
                flags=re.IGNORECASE | re.DOTALL,
            )
        return html

    post.content = remove_from_sections(post.content or "")
    post.save(update_fields=["content"])


class Migration(migrations.Migration):
    dependencies = [
        ("blog", "0033_eliminar_imagenes_antiguas_portabicicletas"),
    ]

    operations = [
        migrations.RunPython(restore_images, remove_images),
    ]
