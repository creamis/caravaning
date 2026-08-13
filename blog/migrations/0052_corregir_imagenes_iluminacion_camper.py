from django.db import migrations

POST_SLUG = "como-mejorar-iluminacion-camper"

# Imágenes verificadas visualmente: todas muestran una camper/autocaravana
# y están directamente relacionadas con iluminación interior o exterior.
IMAGES = [
    "https://resource.iyp.tw/static.iyp.tw/409457/files/246e4e6a-0e06-4d60-b1f2-b338936816cc.jpg",
    "https://www.wingamm.com/wp-content/uploads/2021/09/oasi-690-luxury-camper-drop-bed-216-Modifica-scaled.jpg",
    "https://cdn.shopify.com/s/files/1/0938/0963/9765/collections/TLS_Collection_Images_0002_Outdoor_-_Ambience.webp?v=1749667724",
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
    dependencies = [("blog", "0051_como_mejorar_iluminacion_camper")]
    operations = [migrations.RunPython(replace_images, migrations.RunPython.noop)]
