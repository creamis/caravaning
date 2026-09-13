from django.db import migrations

POST_SLUG = "alquiler-camper-madrid"

GENERATED_IMAGES = [
    "blog_images/generated_madrid/madrid_hero.jpg",
    "blog_images/generated_madrid/madrid_guadarrama.jpg",
    "blog_images/generated_madrid/madrid_segovia.jpg",
    "blog_images/generated_madrid/madrid_ruta.jpg",
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
        ("blog", "0085_alquiler_camper_madrid_camperdays"),
    ]

    operations = [
        migrations.RunPython(add_images, migrations.RunPython.noop),
    ]
