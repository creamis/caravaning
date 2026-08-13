from django.db import migrations

POST_SLUG = "escapada-fin-de-semana-autocaravana"

# Sustituimos únicamente las imágenes 2 y 3.
# Ambas muestran directamente una autocaravana/camper en un entorno de camping.
IMAGES_2_3 = [
    "https://www.balatonbiketour.com/BBTPlacesPictures/958e156a5.jpg",
    "https://prodcdn.phobs.net/1143/rooms/property_31374_1_22Mar23-1648037957.jpg",
]


def replace_images(apps, schema_editor):
    Post = apps.get_model("blog", "Post")
    PostImage = apps.get_model("blog", "PostImage")

    post = Post.objects.filter(slug=POST_SLUG).first()
    if not post:
        return

    images = list(PostImage.objects.filter(post=post).order_by("id"))
    if len(images) < 3:
        return

    images[1].image_url = IMAGES_2_3[0]
    images[1].save(update_fields=["image_url"])
    images[2].image_url = IMAGES_2_3[1]
    images[2].save(update_fields=["image_url"])


class Migration(migrations.Migration):
    dependencies = [
        ("blog", "0056_imagenes_escapada_fin_de_semana_autocaravana"),
    ]

    operations = [
        migrations.RunPython(replace_images, migrations.RunPython.noop),
    ]
