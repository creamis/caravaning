from django.db import migrations

POST_SLUG = "mejores-campings-espana-camper-caravana-autocaravana"

# Imágenes horizontales/relevantes de autocaravanas y caravanas en campings españoles.
# Se añaden como PostImage para que el template del blog las use en el carrusel.
IMAGES = [
    "https://www.turismocostadorada.com/thumbs/default_desktop/643d5268a15a3_2022-camping-las-palmeras00047-1.jpg",
    "https://static.alanrogers.com/images/cache/campsiteimages/ES/ES8/ES83920/2043985/331976126_3022543114714923_100653854749184043_n_8a39923b1b2b.jpg",
    "https://img.sandayagroupe.eu/images/_aliases/embed_accommodation_mobile_20181203_700x434/0/8/7/7/607780-2-fre-FR/e2844ac462e7-Web_crop-VAL_Emplacement_Sud_Premium_003.jpg",
    "https://static.secureholiday.net/static/Pictures/18089/00001354102.jpg?format=webp&width=950",
]


def add_images(apps, schema_editor):
    Post = apps.get_model("blog", "Post")
    PostImage = apps.get_model("blog", "PostImage")

    post = Post.objects.filter(slug=POST_SLUG).first()
    if not post:
        return

    # Esta migración es idempotente respecto al post: elimina solo las imágenes
    # asociadas a este artículo y crea la selección definitiva.
    PostImage.objects.filter(post=post).delete()
    for url in IMAGES:
        PostImage.objects.create(post=post, image_url=url)


class Migration(migrations.Migration):
    dependencies = [
        ("blog", "0058_campings_espana_camping_and_co"),
    ]

    operations = [
        migrations.RunPython(add_images, migrations.RunPython.noop),
    ]
