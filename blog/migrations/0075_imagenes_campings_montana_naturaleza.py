from django.db import migrations

POST_SLUG = "campings-montana-naturaleza-espana"

# Imágenes externas relacionadas directamente con campings de montaña/naturaleza.
# Se mantienen fuera del contenido HTML para que el carrusel del post las gestione.
IMAGES = [
    "https://www.penamontanesa.com/wp-content/uploads/2024/03/mg-742922.jpg",
    "https://campingurbion.com/wp-content/uploads/2024/03/acampada-caravana-3-camping-urbion-soria-1.jpg",
    "https://campingurbion.com/wp-content/uploads/2024/03/ACCESO-DIRECTO-EMBALSE-CAMPING-URBION.jpg",
]


def add_images(apps, schema_editor):
    Post = apps.get_model("blog", "Post")
    PostImage = apps.get_model("blog", "PostImage")

    post = Post.objects.filter(slug=POST_SLUG).first()
    if not post:
        return

    # No borramos imágenes existentes: la migración es conservadora e idempotente.
    for url in IMAGES:
        if not PostImage.objects.filter(post=post, image_url=url).exists():
            PostImage.objects.create(post=post, image_url=url)


class Migration(migrations.Migration):
    dependencies = [
        ("blog", "0074_campings_montana_naturaleza_espana"),
    ]

    operations = [
        migrations.RunPython(add_images, migrations.RunPython.noop),
    ]
