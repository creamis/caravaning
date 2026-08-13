from django.db import migrations

POST_SLUG = "como-mejorar-iluminacion-camper"

# URLs de Wikimedia Commons mediante Special:FilePath.
# Son imágenes reales de interiores de camper/autocaravana y de una autocaravana
# en un entorno nocturno. Special:FilePath evita depender de URLs CDN temporales.
IMAGES = [
    "https://commons.wikimedia.org/wiki/Special:FilePath/Bespoke_Volkswagen_campervan_interior_built_by_The_Wee_Camper_Co..jpg",
    "https://commons.wikimedia.org/wiki/Special:FilePath/Interieur_MRV_L18_-4.jpg",
    "https://commons.wikimedia.org/wiki/Special:FilePath/Kobeta_motorhome_night_view.jpg",
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
    dependencies = [("blog", "0052_corregir_imagenes_iluminacion_camper")]
    operations = [migrations.RunPython(replace_images, migrations.RunPython.noop)]
