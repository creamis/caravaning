from django.db import migrations

POST_SLUG = "alquiler-camper-barcelona"

GENERATED_IMAGES = [
    "blog_images/generated_barcelona/barcelona_hero.jpg",
    "blog_images/generated_barcelona/barcelona_costa_brava.jpg",
    "blog_images/generated_barcelona/barcelona_montseny.jpg",
    "blog_images/generated_barcelona/barcelona_tarragona.jpg",
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
        ("blog", "0087_alquiler_camper_barcelona_camperdays"),
    ]

    operations = [
        migrations.RunPython(add_images, migrations.RunPython.noop),
    ]
