from django.db import migrations

POST_SLUG = "portabicicletas-camper-autocaravana"

FIAMMA_OLD = "https://m.media-amazon.com/images/I/61OwXeRNDRL._AC_SL1500_.jpg"
FIAMMA_NEW = "https://www.agentfiamma.co.uk/images/D/carry-bike-pro-c-2023.jpg"

THULE_OLD = "https://shop.freizeit-wittke.eu/media/image/product/198266/lg/thule-fahrradtraeger-elite-van-xt-fuer-fiat-ducato-ab-bj-2007-schwarz.jpg"
THULE_NEW = "https://www.camperpassie.nl/media/catalog/product/cache/207e23213cf636ccdef205098cf3c8a3/t/h/thule-elite-van-xt-camperpassie_2.jpg"


def update_images(apps, schema_editor):
    Post = apps.get_model("blog", "Post")
    PostImage = apps.get_model("blog", "PostImage")

    try:
        post = Post.objects.get(slug=POST_SLUG)
    except Post.DoesNotExist:
        return

    # Replace the URLs embedded in the article body as well as the PostImage
    # records. This is necessary because the article uses both mechanisms.
    content = post.content or ""
    content = content.replace(FIAMMA_OLD, FIAMMA_NEW)
    content = content.replace(THULE_OLD, THULE_NEW)
    post.content = content
    post.save(update_fields=["content"])

    # Remove the two old image records and ensure the new product-specific
    # photographs are present. Keep the rest of the article images untouched.
    PostImage.objects.filter(post=post, image_url=FIAMMA_OLD).delete()
    PostImage.objects.filter(post=post, image_url=THULE_OLD).delete()
    PostImage.objects.get_or_create(post=post, image_url=FIAMMA_NEW)
    PostImage.objects.get_or_create(post=post, image_url=THULE_NEW)


def reverse_update_images(apps, schema_editor):
    Post = apps.get_model("blog", "Post")
    PostImage = apps.get_model("blog", "PostImage")

    try:
        post = Post.objects.get(slug=POST_SLUG)
    except Post.DoesNotExist:
        return

    content = post.content or ""
    content = content.replace(FIAMMA_NEW, FIAMMA_OLD)
    content = content.replace(THULE_NEW, THULE_OLD)
    post.content = content
    post.save(update_fields=["content"])

    PostImage.objects.filter(post=post, image_url=FIAMMA_NEW).delete()
    PostImage.objects.filter(post=post, image_url=THULE_NEW).delete()
    PostImage.objects.get_or_create(post=post, image_url=FIAMMA_OLD)
    PostImage.objects.get_or_create(post=post, image_url=THULE_OLD)


class Migration(migrations.Migration):
    dependencies = [("blog", "0031_actualizar_imagenes_portabicicletas")]

    operations = [migrations.RunPython(update_images, reverse_update_images)]
