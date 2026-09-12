from decimal import Decimal
from django.db import migrations


# Precios comprobados en Decathlon España en septiembre de 2026.
# Se guardan como orientativos porque pueden cambiar en el comercio.
PRODUCT_PRICES = [
    (["BL100", "Lámpara", "Lampara"], Decimal("9.99")),
    (["Ice Compact", "Mochila nevera", "nevera 30"], Decimal("34.99")),
    (["Mueble de cocina", "mueble cocina"], Decimal("84.99")),
    (["Silla plegable", "Quechua Basic"], Decimal("17.99")),
    (["Mesa plegable", "2 a 4 personas"], Decimal("19.99")),
]


def update_decathlon_prices(apps, schema_editor):
    Product = apps.get_model("shop", "Product")

    products = Product.objects.filter(merchant_name__iexact="Decathlon")

    for product in products:
        haystack = f"{product.name} {product.description}".lower()
        for terms, price in PRODUCT_PRICES:
            if any(term.lower() in haystack for term in terms):
                product.price = price
                product.price_note = f"{str(price).replace('.', ',')} € aprox. · consulta el precio actual en Decathlon"
                product.button_text = "Ver precio actual en Decathlon"
                product.save(update_fields=["price", "price_note", "button_text"])
                break


class Migration(migrations.Migration):
    dependencies = [
        ("shop", "0006_decathlon_deep_links_images"),
    ]

    operations = [
        migrations.RunPython(update_decathlon_prices, migrations.RunPython.noop),
    ]
