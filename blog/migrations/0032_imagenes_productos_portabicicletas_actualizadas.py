import re

from django.db import migrations

POST_SLUG = "portabicicletas-camper-autocaravana"

FIAMMA_IMAGE = "https://shop.rvsupercentre.co.nz/cdn/shop/files/Pro-1.jpg?v=1774836155"
THULE_IMAGE = "https://kombilife.com.au/cdn/shop/files/Kombilife-VW-Crafter-Thule-elite-Van-xt-black-photo13_1158x812.jpg?v=1721953742"


def replace_product_image(html, heading, image_url, alt):
    """Replace every image inside one product section, regardless of its old URL."""
    pattern = rf"(<h2>\s*{re.escape(heading)}\s*</h2>)(.*?)(?=<h2>|\Z)"

    def repl(match):
        section = match.group(2)
        section = re.sub(r'<img\b[^>]*>', '', section, flags=re.IGNORECASE)
        image = (
            f'<img src="{image_url}" alt="{alt}" loading="lazy" '
            'style="display:block;width:100%;max-width:100%;aspect-ratio:16/9;'
            'height:auto;object-fit:contain;border-radius:16px;margin:18px 0;">'
        )
        return match.group(1) + section.replace('</p>', f'</p>{image}', 1)

    return re.sub(pattern, repl, html, flags=re.IGNORECASE | re.DOTALL)


def update_images(apps, schema_editor):
    Post = apps.get_model("blog", "Post")
    PostImage = apps.get_model("blog", "PostImage")

    post = Post.objects.filter(slug=POST_SLUG).first()
    if not post:
        return

    content = post.content or ""
    content = replace_product_image(
        content,
        "1. Fiamma Carry-Bike para autocaravana y camper",
        FIAMMA_IMAGE,
        "Fiamma Carry-Bike Pro C para autocaravana y camper",
    )
    content = replace_product_image(
        content,
        "2. Thule Elite Van XT",
        THULE_IMAGE,
        "Thule Elite Van XT instalado en una furgoneta camper",
    )
    post.content = content
    post.save(update_fields=["content"])

    # Remove the old image records for these two sections and keep only the
    # current product photographs. No alt_text is passed because PostImage
    # does not define that field in the current project.
    PostImage.objects.filter(post=post).filter(
        image_url__in=[FIAMMA_IMAGE, THULE_IMAGE]
    ).delete()

    # Remove any previous image records whose URL contains the old product
    # image hosts/paths, then add the two current photographs.
    for image in PostImage.objects.filter(post=post):
        url = image.image_url or ""
        if (
            "61OwXeRNDRL" in url
            or "thule-fahrradtraeger-elite-van-xt" in url
            or "Kombilife-VW-Crafter-Thule-elite-Van-xt" in url
            or "shop.rvsupercentre.co.nz" in url
        ):
            image.delete()

    PostImage.objects.get_or_create(post=post, image_url=FIAMMA_IMAGE)
    PostImage.objects.get_or_create(post=post, image_url=THULE_IMAGE)


def reverse_images(apps, schema_editor):
    Post = apps.get_model("blog", "Post")
    PostImage = apps.get_model("blog", "PostImage")
    post = Post.objects.filter(slug=POST_SLUG).first()
    if not post:
        return

    PostImage.objects.filter(post=post, image_url__in=[FIAMMA_IMAGE, THULE_IMAGE]).delete()


class Migration(migrations.Migration):
    dependencies = [
        ("blog", "0031_actualizar_imagenes_portabicicletas"),
    ]

    operations = [
        migrations.RunPython(update_images, reverse_images),
    ]
