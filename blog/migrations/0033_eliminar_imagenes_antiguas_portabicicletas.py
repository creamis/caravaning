from django.db import migrations
import re

POST_SLUG = "portabicicletas-camper-autocaravana"


def remove_product_images(html):
    """Remove embedded images from the two affected product sections.

    The article keeps its text and Amazon links. We deliberately remove the
    images from these sections because the available photographs are not
    reliable representations of the products.
    """
    headings = [
        "1. Fiamma Carry-Bike para autocaravana y camper",
        "2. Thule Elite Van XT",
    ]

    for heading in headings:
        pattern = rf"(<h2>\s*{re.escape(heading)}\s*</h2>)(.*?)(?=<h2>|\Z)"

        def repl(match):
            section = match.group(2)
            section = re.sub(r"<img\b[^>]*>", "", section, flags=re.IGNORECASE)
            return match.group(1) + section

        html = re.sub(pattern, repl, html, flags=re.IGNORECASE | re.DOTALL)

    return html


def remove_old_images(apps, schema_editor):
    Post = apps.get_model("blog", "Post")
    PostImage = apps.get_model("blog", "PostImage")

    post = Post.objects.filter(slug=POST_SLUG).first()
    if not post:
        return

    # Remove the old carousel/cover images, including the generic Amazon
    # placeholder that was being shown at the top of the article.
    PostImage.objects.filter(post=post).delete()

    # Remove the embedded photographs from the two product sections.
    post.content = remove_product_images(post.content or "")
    post.save(update_fields=["content"])


def restore_images(apps, schema_editor):
    # Intentionally left empty. The removed photographs were incorrect or
    # obsolete and should not be restored automatically on a rollback.
    pass


class Migration(migrations.Migration):
    dependencies = [
        ("blog", "0032_imagenes_productos_portabicicletas_actualizadas"),
    ]

    operations = [
        migrations.RunPython(remove_old_images, restore_images),
    ]
