from django.db import migrations

POST_SLUG = "como-mejorar-iluminacion-camper"
IMAGES = [
    "https://cdn.shopify.com/s/files/1/0969/5444/files/RV-Interior-Ceiling-White-LED-Lights-_Pair_-Nilight-51992774.jpg?v=1732245807",
    "https://sereneandspace.com/img/image4_sprinter-van-interiors-ideas_ambient-lighting.jpg",
    "https://cdn.webshopapp.com/shops/354950/files/491985159/led-beleuchtung-markise-wohnmobil.jpg",
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
    dependencies = [("blog", "0053_imagenes_iluminacion_camper_wikimedia")]
    operations = [migrations.RunPython(replace_images, migrations.RunPython.noop)]
