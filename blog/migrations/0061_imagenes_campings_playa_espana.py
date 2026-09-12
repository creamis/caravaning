from django.db import migrations

POST_SLUG = "mejores-campings-playa-espana-camper-caravana-autocaravana"

IMAGES = [
    "https://www.turismocostadorada.com/thumbs/default_desktop/643d5268a15a3_2022-camping-las-palmeras00047-1.jpg",
    "https://images.twentycdn.net/sites/42a5ba334b176.original.jpg",
    "https://cdn2.acsi.eu/6/9/3/3/6933d1d8d4dfd.jpeg?impolicy=gallery-detail",
    "https://static.secureholiday.net/static/Pictures/438/00000520312.jpg?width=800",
]


def add_images(apps, schema_editor):
    Post = apps.get_model("blog", "Post")
    PostImage = apps.get_model("blog", "PostImage")

    post = Post.objects.filter(slug=POST_SLUG).first()
    if not post:
        return

    for image_url in IMAGES:
        PostImage.objects.get_or_create(
            post=post,
            image_url=image_url,
        )


class Migration(migrations.Migration):
    dependencies = [
        ("blog", "0060_campings_playa_espana_camping_and_co"),
    ]

    operations = [
        migrations.RunPython(add_images, migrations.RunPython.noop),
    ]
