from django.db import migrations

POST_SLUG = "alquiler-camper-valencia"

# Las imágenes generadas para CamperDays Valencia se sirven desde /static/.
# PythonAnywhere ya sirve /static/ correctamente, por lo que evitamos depender
# de la configuración de /media/ para estas imágenes editoriales.
STATIC_IMAGES = [
    "/static/images/blog/camperdays/valencia/valencia_hero.jpg",
    "/static/images/blog/camperdays/valencia/valencia_playa.jpg",
    "/static/images/blog/camperdays/valencia/valencia_albufera.jpg",
    "/static/images/blog/camperdays/valencia/valencia_ruta.jpg",
]


def replace_images(apps, schema_editor):
    Post = apps.get_model("blog", "Post")
    PostImage = apps.get_model("blog", "PostImage")

    post = Post.objects.filter(slug=POST_SLUG).first()
    if not post:
        return

    PostImage.objects.filter(post=post).delete()

    for url in STATIC_IMAGES:
        PostImage.objects.create(
            post=post,
            image="",
            image_url=url,
        )


class Migration(migrations.Migration):
    dependencies = [
        ("blog", "0082_imagenes_generadas_alquiler_camper_valencia"),
    ]

    operations = [
        migrations.RunPython(replace_images, migrations.RunPython.noop),
    ]
