from django.db import migrations

POST_SLUG = "alquiler-camper-valencia"

GENERATED_IMAGES = [
    "blog_images/generated_valencia/valencia_hero.jpg",
    "blog_images/generated_valencia/valencia_playa.jpg",
    "blog_images/generated_valencia/valencia_albufera.jpg",
    "blog_images/generated_valencia/valencia_ruta.jpg",
]


def replace_images(apps, schema_editor):
    Post = apps.get_model("blog", "Post")
    PostImage = apps.get_model("blog", "PostImage")

    post = Post.objects.filter(slug=POST_SLUG).first()
    if not post:
        return

    # Sustituir todas las imágenes anteriores del post por las generadas
    # específicamente para esta guía de Valencia.
    PostImage.objects.filter(post=post).delete()

    for image_path in GENERATED_IMAGES:
        PostImage.objects.create(
            post=post,
            image=image_path,
            image_url=None,
        )


class Migration(migrations.Migration):
    dependencies = [
        ("blog", "0081_mejorar_imagenes_alquiler_camper_valencia"),
    ]

    operations = [
        migrations.RunPython(replace_images, migrations.RunPython.noop),
    ]
