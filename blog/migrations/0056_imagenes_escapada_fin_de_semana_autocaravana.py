from django.db import migrations

POST_SLUG = "escapada-fin-de-semana-autocaravana"

# Imágenes seleccionadas específicamente para este artículo:
# 1) interior de una camper en contexto de viaje/camping (2026)
# 2) zona de camping para caravanas y autocaravanas (2026)
# 3) área real de autocaravanas en España (2025)
# Se usa Special:Redirect/file de Wikimedia Commons para apuntar al archivo real.
IMAGES = [
    "https://commons.wikimedia.org/wiki/Special:Redirect/file/Camper%20van%20with%20family%20inside%20playing%20games.jpg",
    "https://commons.wikimedia.org/wiki/Special:Redirect/file/New%20Camping%20Area%20at%20the%20Caravan%20and%20Motorhome%20Club%20Site%20-%20geograph.org.uk%20-%208341704.jpg",
    "https://commons.wikimedia.org/wiki/Special:Redirect/file/%C3%81rea%20de%20autocaravanas%20en%20Lagr%C3%A1n.jpg",
]


def replace_images(apps, schema_editor):
    Post = apps.get_model("blog", "Post")
    PostImage = apps.get_model("blog", "PostImage")

    post = Post.objects.filter(slug=POST_SLUG).first()
    if not post:
        return

    PostImage.objects.filter(post=post).delete()
    for url in IMAGES:
        PostImage.objects.create(post=post, image_url=url)


class Migration(migrations.Migration):
    dependencies = [
        ("blog", "0055_escapada_fin_de_semana_autocaravana"),
    ]

    operations = [
        migrations.RunPython(replace_images, migrations.RunPython.noop),
    ]
