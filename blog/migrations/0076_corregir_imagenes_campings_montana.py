from django.db import migrations

POST_SLUG = "campings-montana-naturaleza-espana"

BROKEN_IMAGES = [
    "https://www.penamontanesa.com/wp-content/uploads/2024/03/mg-742922.jpg",
    "https://campingurbion.com/wp-content/uploads/2024/03/acampada-caravana-3-camping-urbion-soria-1.jpg",
    "https://campingurbion.com/wp-content/uploads/2024/03/ACCESO-DIRECTO-EMBALSE-CAMPING-URBION.jpg",
]

# Wikimedia Commons mediante Special:FilePath. Este formato ya se utiliza en otros
# posts del proyecto y evita depender del hotlinking de webs comerciales.
IMAGES = [
    "https://commons.wikimedia.org/wiki/Special:FilePath/Archena%20MH%20stopover%20mountains.jpg",
    "https://commons.wikimedia.org/wiki/Special:FilePath/Camping%20site%20in%20northern%20Spain%201994.jpg",
    "https://commons.wikimedia.org/wiki/Special:FilePath/Campingplatz%20Despenaperros%20in%20E%2023213%20Santa%20Elena%20-%20panoramio%20-%20Karl-Heinz%20B%C3%B6hm.jpg",
]


def replace_images(apps, schema_editor):
    Post = apps.get_model("blog", "Post")
    PostImage = apps.get_model("blog", "PostImage")

    post = Post.objects.filter(slug=POST_SLUG).first()
    if not post:
        return

    PostImage.objects.filter(post=post, image_url__in=BROKEN_IMAGES).delete()

    for url in IMAGES:
        if not PostImage.objects.filter(post=post, image_url=url).exists():
            PostImage.objects.create(post=post, image_url=url)


class Migration(migrations.Migration):
    dependencies = [
        ("blog", "0075_imagenes_campings_montana_naturaleza"),
    ]

    operations = [
        migrations.RunPython(replace_images, migrations.RunPython.noop),
    ]
