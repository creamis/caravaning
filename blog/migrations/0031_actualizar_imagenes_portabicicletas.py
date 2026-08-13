from django.db import migrations

POST_SLUG = "portabicicletas-camper-autocaravana"

OLD_FIAMMA = "https://m.media-amazon.com/images/I/61OwXeRNDRL._AC_SL1500_.jpg"
NEW_FIAMMA = "https://shop.rvsupercentre.co.nz/cdn/shop/files/Pro-1.jpg?v=1774836155"

OLD_THULE = "https://shop.freizeit-wittke.eu/media/image/product/198266/lg/thule-fahrradtraeger-elite-van-xt-fuer-fiat-ducato-ab-bj-2007-schwarz.jpg"
NEW_THULE = "https://kombilife.com.au/cdn/shop/files/Kombilife-VW-Crafter-Thule-elite-Van-xt-black-photo13_1158x812.jpg?v=1721953742"


def update_images(apps, schema_editor):
    Post = apps.get_model("blog", "Post")
    PostImage = apps.get_model("blog", "PostImage")

    post = Post.objects.filter(slug=POST_SLUG).first()
    if not post:
        return

    # Replace the two outdated images inside the published article.
    post.content = post.content.replace(OLD_FIAMMA, NEW_FIAMMA)
    post.content = post.content.replace(OLD_THULE, NEW_THULE)
    post.save(update_fields=["content"])

    # Remove the old gallery entries and add the current product photographs.
    PostImage.objects.filter(post=post, image_url=OLD_FIAMMA).delete()
    PostImage.objects.filter(post=post, image_url=OLD_THULE).delete()

    PostImage.objects.get_or_create(post=post, image_url=NEW_FIAMMA)
    PostImage.objects.get_or_create(post=post, image_url=NEW_THULE)


def reverse_update_images(apps, schema_editor):
    Post = apps.get_model("blog", "Post")
    PostImage = apps.get_model("blog", "PostImage")

    post = Post.objects.filter(slug=POST_SLUG).first()
    if not post:
        return

    post.content = post.content.replace(NEW_FIAMMA, OLD_FIAMMA)
    post.content = post.content.replace(NEW_THULE, OLD_THULE)
    post.save(update_fields=["content"])

    PostImage.objects.filter(post=post, image_url=NEW_FIAMMA).delete()
    PostImage.objects.filter(post=post, image_url=NEW_THULE).delete()


class Migration(migrations.Migration):
    dependencies = [("blog", "0030_imagenes_estacionales_caravaning")]

    operations = [
        migrations.RunPython(update_images, reverse_update_images),
    ]
