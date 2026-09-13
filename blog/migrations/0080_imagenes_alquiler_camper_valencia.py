from django.db import migrations

POST_SLUG = "alquiler-camper-valencia"

IMAGES = [
    "https://commons.wikimedia.org/wiki/Special:FilePath/1996%20Fiat%20146L%20motorhome%20camper%20van%20%2815038760770%29.jpg",
    "https://commons.wikimedia.org/wiki/Special:FilePath/Valencia%20Beach.jpg",
    "https://commons.wikimedia.org/wiki/Special:FilePath/Albufera%20Valencia.jpg",
    "https://commons.wikimedia.org/wiki/Special:FilePath/Pe%C3%B1iscola.jpg",
]


def add_images(apps, schema_editor):
    Post = apps.get_model("blog", "Post")
    PostImage = apps.get_model("blog", "PostImage")

    post = Post.objects.filter(slug=POST_SLUG).first()
    if not post:
        return

    for url in IMAGES:
        if not PostImage.objects.filter(post=post, image_url=url).exists():
            PostImage.objects.create(post=post, image_url=url)


class Migration(migrations.Migration):
    dependencies = [
        ("blog", "0079_alquiler_camper_valencia_camperdays"),
    ]

    operations = [
        migrations.RunPython(add_images, migrations.RunPython.noop),
    ]
