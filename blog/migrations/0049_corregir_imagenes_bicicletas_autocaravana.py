from django.db import migrations

POST_SLUG = "como-llevar-bicicletas-autocaravana"

IMAGES = [
    "https://www.wohnmobilforum.de/bilderdienst/wohnmobile/Carrybike_5e65.jpg",
    "https://www.motorhomefun.co.uk/forum/attachments/pxl_20210801_122625524_original-jpg.528579/",
    "https://todocampers.com/58718-large_default/portabicicletas-fiamma-carry-bike-dj-para-ducato-jumper-y-boxer-desde-2007-y-movano-desde-2021-2-bicis.jpg",
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
    dependencies = [("blog", "0048_como_llevar_bicicletas_autocaravana")]
    operations = [migrations.RunPython(replace_images, migrations.RunPython.noop)]
