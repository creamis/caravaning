from django.db import migrations

POST_SLUG = "alquiler-camper-valencia"

OLD_IMAGES = [
    "https://commons.wikimedia.org/wiki/Special:FilePath/1996%20Fiat%20146L%20motorhome%20camper%20van%20%2815038760770%29.jpg",
    "https://commons.wikimedia.org/wiki/Special:FilePath/Valencia%20Beach.jpg",
    "https://commons.wikimedia.org/wiki/Special:FilePath/Albufera%20Valencia.jpg",
    "https://commons.wikimedia.org/wiki/Special:FilePath/Pe%C3%B1iscola.jpg",
]

# Nueva línea visual: camper/autocaravana moderna, protagonista y en entornos agradables.
# Todas las imágenes proceden de Wikimedia Commons y usan Special:FilePath.
NEW_IMAGES = [
    "https://commons.wikimedia.org/wiki/Special:FilePath/Motorhome%20at%20the%20Beach%20%E2%80%93%20Sunset%20by%20the%20Sea.png",
    "https://commons.wikimedia.org/wiki/Special:FilePath/Man%20sits%20next%20to%20camper%20van%20while%20resting%20and%20enjoying%20outdoor%20time%20in%20warm%20weather%20on%20a%20clear%20day.jpg",
    "https://commons.wikimedia.org/wiki/Special:FilePath/Man%20sets%20up%20awning%20for%20camper%20van%20near%20mountains%20in%20daylight%20while%20preparing%20for%20a%20trip%20to%20nature.jpg",
    "https://commons.wikimedia.org/wiki/Special:FilePath/Man%20moves%20chair%20in%20camper%20van%20while%20preparing%20for%20outdoor%20activity%20on%20a%20sunny%20day%20in%20a%20natural%20setting.jpg",
]


def replace_images(apps, schema_editor):
    Post = apps.get_model("blog", "Post")
    PostImage = apps.get_model("blog", "PostImage")

    post = Post.objects.filter(slug=POST_SLUG).first()
    if not post:
        return

    # Quitar únicamente las cuatro imágenes introducidas por 0080.
    PostImage.objects.filter(post=post, image_url__in=OLD_IMAGES).delete()

    # Evitar duplicados si la migración se ejecuta en un entorno parcialmente preparado.
    for url in NEW_IMAGES:
        if not PostImage.objects.filter(post=post, image_url=url).exists():
            PostImage.objects.create(post=post, image_url=url)


class Migration(migrations.Migration):
    dependencies = [
        ("blog", "0080_imagenes_alquiler_camper_valencia"),
    ]

    operations = [
        migrations.RunPython(replace_images, migrations.RunPython.noop),
    ]
