from django.db import migrations

POST_SLUG = "alquiler-camper-sevilla"

GENERATED_IMAGES = [
    "blog_images/generated_sevilla/sevilla_hero.jpg",
    "blog_images/generated_sevilla/sevilla_sierra_norte.jpg",
    "blog_images/generated_sevilla/sevilla_pueblos.jpg",
    "blog_images/generated_sevilla/sevilla_ruta.jpg",
]


def add_images(apps, schema_editor):
    Post = apps.get_model("blog", "Post")
    PostImage = apps.get_model("blog", "PostImage")

    post = Post.objects.filter(slug=POST_SLUG).first()
    if not post:
        return

    PostImage.objects.filter(post=post).delete()

    for image_path in GENERATED_IMAGES:
        PostImage.objects.create(
            post=post,
            image=image_path,
            image_url=None,
        )


class Migration(migrations.Migration):
    dependencies = [
        ("blog", "0091_alquiler_camper_sevilla_camperdays"),
    ]

    operations = [
        migrations.RunPython(add_images, migrations.RunPython.noop),
    ]
