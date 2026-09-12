from django.db import migrations


LAMP_IMAGE_URL = (
    "https://contents.mediadecathlon.com/p1721776/"
    "k%240c96511dcc1b7670e777039e9b504d5e/"
    "lampe-de-camping-bl100-100-lumens.jpg"
)


def add_bl100_image(apps, schema_editor):
    Product = apps.get_model("shop", "Product")
    ProductImage = apps.get_model("shop", "ProductImage")

    product = (
        Product.objects.filter(name__icontains="BL100").first()
        or Product.objects.filter(name__icontains="Lampara de camping").first()
        or Product.objects.filter(name__icontains="Lámpara de camping").first()
    )

    if not product:
        return

    product.image_url = LAMP_IMAGE_URL
    product.save(update_fields=["image_url"])

    ProductImage.objects.get_or_create(
        product=product,
        image_url=LAMP_IMAGE_URL,
    )


class Migration(migrations.Migration):
    dependencies = [
        ("shop", "0007_precios_decathlon"),
    ]

    operations = [
        migrations.RunPython(add_bl100_image, migrations.RunPython.noop),
    ]
