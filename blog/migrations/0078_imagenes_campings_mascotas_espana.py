from django.db import migrations

POST_SLUG = "campings-admiten-mascotas-espana"

# Imágenes horizontales y temáticamente coherentes con viajar/campar con perro.
# Wikimedia Commons mediante Special:FilePath para evitar depender del hotlinking
# de webs comerciales.
IMAGES = [
    "https://commons.wikimedia.org/wiki/Special:FilePath/Caravan%20with%20new%20Kampa%20Inflatable%20Awning%20and%20Micha%20the%20Boxer%20Dog%20%2815123465967%29.jpg",
    "https://commons.wikimedia.org/wiki/Special:FilePath/Camp%20dog.jpg",
    "https://commons.wikimedia.org/wiki/Special:FilePath/Camping%20with%20dog%20alone%20under%20the%20sky%20in%20the%20tent%20%283%29%2012.jpg",
    "https://commons.wikimedia.org/wiki/Special:FilePath/Camping%20in%20tent%20alone%20under%20the%20sky%20in%20night%20with%20dog%20%282%29%2026.jpg",
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
        ("blog", "0077_campings_mascotas_espana"),
    ]

    operations = [
        migrations.RunPython(add_images, migrations.RunPython.noop),
    ]
