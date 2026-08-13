from django.db import migrations

POST_SLUG = "como-llevar-bicicletas-autocaravana"

# URLs comprobadas como archivos de imagen y relacionadas directamente
# con el transporte de bicicletas en camper/autocaravana.
IMAGES = [
    "https://www.wohnmobilforum.de/bilderdienst/wohnmobile/Carrybike_5e65.jpg",
    "https://cdn.wisselinkcaravans.nl/291055/conversions/sMJPHjjJRN9p8E8XO8mEIEcffH1dyfJx850PcGLw-thumb.jpg",
    "https://i0.wp.com/everythingfiamma.co.uk/wp-content/uploads/2021/05/Lift-77-02096-44-12218-24-2.jpg?fit=780%2C866&ssl=1",
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
    dependencies = [("blog", "0049_corregir_imagenes_bicicletas_autocaravana")]
    operations = [migrations.RunPython(replace_images, migrations.RunPython.noop)]
