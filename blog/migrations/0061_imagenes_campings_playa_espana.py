from django.db import migrations

POST_SLUG = "mejores-campings-playa-espana-camper-caravana-autocaravana"

IMAGES = [
    (
        "https://www.turismocostadorada.com/thumbs/default_desktop/643d5268a15a3_2022-camping-las-palmeras00047-1.jpg",
        "Camping junto a la playa con caravanas y autocaravanas en la Costa Dorada",
    ),
    (
        "https://images.twentycdn.net/sites/42a5ba334b176.original.jpg",
        "Parcelas de camping con caravanas junto a una playa de la Costa Brava",
    ),
    (
        "https://cdn2.acsi.eu/6/9/3/3/6933d1d8d4dfd.jpeg?impolicy=gallery-detail",
        "Vista aérea de un camping costero con caravanas y playa en Girona",
    ),
    (
        "https://static.secureholiday.net/static/Pictures/438/00000520312.jpg?width=800",
        "Caravana instalada entre palmeras en un camping junto al Mediterráneo",
    ),
]


def add_images(apps, schema_editor):
    Post = apps.get_model("blog", "Post")
    PostImage = apps.get_model("blog", "PostImage")

    post = Post.objects.filter(slug=POST_SLUG).first()
    if not post:
        return

    # Only manage external images added for this article. Using get_or_create
    # keeps the migration safe if it is ever run against data that already
    # contains one of these URLs.
    for image_url, alt_text in IMAGES:
        PostImage.objects.get_or_create(
            post=post,
            image_url=image_url,
            defaults={"alt_text": alt_text},
        )


class Migration(migrations.Migration):
    dependencies = [
        ("blog", "0060_campings_playa_espana_camping_and_co"),
    ]

    operations = [
        migrations.RunPython(add_images, migrations.RunPython.noop),
    ]
