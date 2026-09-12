from django.db import migrations
from urllib.parse import quote

AWIN_MID = "105405"
AWIN_AFFID = "2917197"

PRODUCTS = [
    {
        "name_contains": "Lampara de camping recargable Quechua BL100",
        "destination": "https://www.decathlon.es/es/p/lampara-de-camping-100-lumenes-ipx4-pilas-incluidas-quechua-bl100/172514/c98c66m8492468",
        "image_url": None,
    },
    {
        "name_contains": "Mochila nevera Quechua Ice Compact 30 L",
        "destination": "https://www.decathlon.es/es/p/mochila-nevera-30l-quechua-ice-compact/309970/c328m8913720",
        "image_url": "https://contents.mediadecathlon.com/p2837133/k%243a81aef5237cc599943bb1a70022209a/picture.jpg?f=3000x0&format=auto",
    },
    {
        "name_contains": "Mueble de cocina camping Quechua",
        "destination": "https://www.decathlon.es/es/p/mueble-de-cocina-de-camping-l-plegable-y-con-mampara/354898/m8882499",
        "image_url": "https://contents.mediadecathlon.com/p2999833/k%2488269d9c4fc2ffc56496674dd0812124/picture.jpg?f=3000x0&format=auto",
    },
    {
        "name_contains": "Silla plegable camping Quechua con reposabrazos",
        "destination": "https://www.decathlon.es/es/p/silla-plegable-de-camping-con-reposabrazos-quechua-basic/13372/c98m8852991",
        "image_url": "https://contents.mediadecathlon.com/p2598175/k%24ef0cd18cf948c705e900c9cf2e92dc64/picture.jpg?f=3000x0&format=auto",
    },
    {
        "name_contains": "Mesa plegable camping 4 personas Quechua",
        "destination": "https://www.decathlon.es/es/p/mesa-plegable-de-camping-4-personas-marron/303341/c14m8950609",
        "image_url": "https://contents.mediadecathlon.com/p3088743/k%2475e2fa1fcc604d69ff3503ce69de2cec/picture.jpg?f=3000x0&format=auto",
    },
]


def awin(destination):
    return (
        "https://www.awin1.com/cread.php?"
        f"awinmid={AWIN_MID}&awinaffid={AWIN_AFFID}&ued={quote(destination, safe='')}"
    )


def update_decathlon_products(apps, schema_editor):
    Product = apps.get_model("shop", "Product")
    ProductImage = apps.get_model("shop", "ProductImage")

    for item in PRODUCTS:
        product = Product.objects.filter(name__icontains=item["name_contains"]).first()
        if not product:
            continue

        product.merchant_name = "Decathlon"
        product.affiliate_url = awin(item["destination"])
        product.button_text = "Ver en Decathlon"
        product.is_affiliate = True
        product.price_note = "Consultar en Decathlon"

        if item["image_url"]:
            product.image_url = item["image_url"]

        product.save()

        if item["image_url"]:
            ProductImage.objects.get_or_create(
                product=product,
                image_url=item["image_url"],
            )


class Migration(migrations.Migration):
    dependencies = [
        ("shop", "0005_product_best_for_product_is_affiliate_and_more"),
    ]

    operations = [
        migrations.RunPython(update_decathlon_products, migrations.RunPython.noop),
    ]
