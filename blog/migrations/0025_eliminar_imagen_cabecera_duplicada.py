from django.db import migrations

POST_SLUGS = [
    "tpms-caravana-autocaravana-monitor-presion-neumaticos",
    "como-nivelar-caravana-calzos-rampas-nivel",
    "agua-caravana-depositos-bombas-bidones-accesorios",
    "wc-portatil-camping-camper-caravana-guia-compra",
    "toldo-avance-caravana-guia-compra",
]


def remove_duplicate_header_images(apps, schema_editor):
    Post = apps.get_model("blog", "Post")

    for slug in POST_SLUGS:
        post = Post.objects.filter(slug=slug).first()
        if not post:
            continue

        content = post.content or ""

        # 0023 inserted the same image both in PostImage (used by the
        # carousel/header) and at the beginning of post.content. Keep the
        # PostImage version and remove only the embedded figure.
        start = content.find("<figure")
        if start == -1:
            continue

        end = content.find("</figure>", start)
        if end == -1:
            continue

        figure = content[start:end + len("</figure>")]
        if "Imagen ilustrativa." in figure:
            content = content[:start] + content[end + len("</figure"):]
            post.content = content.lstrip()
            post.save(update_fields=["content", "updated_at"])


def reverse_remove_duplicate_header_images(apps, schema_editor):
    pass


class Migration(migrations.Migration):
    dependencies = [("blog", "0024_quitar_aviso_afiliado_superior")]

    operations = [
        migrations.RunPython(
            remove_duplicate_header_images,
            reverse_remove_duplicate_header_images,
        )
    ]
