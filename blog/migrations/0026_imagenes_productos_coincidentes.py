from django.db import migrations

GUIDES = {
    "tpms-caravana-autocaravana-monitor-presion-neumaticos": {
        "image": "https://www.tiremoni.com/wp-content/uploads/2017/10/tm-260R-neu-rgb72dpi.jpg",
        "credit": "TireMoni TM-260R Professional, fotografía de producto de TireMoni",
        "amazon": "https://www.amazon.es/s?k=TireMoni+TM-260R&tag=caravaning0a-21",
        "product": "TireMoni TM-260R",
    },
    "como-nivelar-caravana-calzos-rampas-nivel": {
        "image": "https://marine-deals-io.freetls.fastly.net/media/catalog/product/1/1/112714_1_pc.jpg?dpr=2&filter=lanczos&fit=bounds&format=webp&height=500&width=500",
        "credit": "Milenco Quattro Levellers, fotografía de producto de Marine-Deals",
        "amazon": "https://www.amazon.es/s?k=Milenco+Quattro+3+caravana&tag=caravaning0a-21",
        "product": "Milenco Quattro 3",
    },
    "agua-caravana-depositos-bombas-bidones-accesorios": {
        "image": "https://nomadicleisure.co.uk/wp-content/uploads/2023/10/Whale-Watermaster-On-Board-Pump-1-1024x1024.jpg",
        "credit": "Whale Watermaster On Board Pump, fotografía de producto de Nomadic Leisure",
        "amazon": "https://www.amazon.es/s?k=Whale+Watermaster+caravana&tag=caravaning0a-21",
        "product": "Whale Watermaster",
    },
    "wc-portatil-camping-camper-caravana-guia-compra": {
        "image": "https://destinazionecamper.com/cdn/shop/products/portapottithetford165.jpg?v=1662665928",
        "credit": "Thetford Porta Potti 165, fotografía de producto de Destinazione Camper",
        "amazon": "https://www.amazon.es/s?k=Thetford+Porta+Potti+165&tag=caravaning0a-21",
        "product": "Thetford Porta Potti 165",
    },
    "toldo-avance-caravana-guia-compra": {
        "image": "https://cdn11.bigcommerce.com/s-u2qvrsnw19/images/stencil/1280x1280/products/4389/15862/F80s-T__95271.1655483320.png?c=2",
        "credit": "Fiamma F80s, fotografía de producto de Panther RV Products",
        "amazon": "https://www.amazon.es/s?k=Fiamma+F80s+toldo&tag=caravaning0a-21",
        "product": "Fiamma F80s",
    },
}


def replace_images(apps, schema_editor):
    Post = apps.get_model("blog", "Post")
    PostImage = apps.get_model("blog", "PostImage")

    for slug, data in GUIDES.items():
        post = Post.objects.filter(slug=slug).first()
        if not post:
            continue

        PostImage.objects.filter(post=post).delete()
        PostImage.objects.create(post=post, image_url=data["image"])

        marker = "<section><h2>🛒 Productos que puedes consultar en Amazon</h2>"
        if marker in post.content and data["amazon"] not in post.content:
            card = (
                f"<div style='margin:1rem 0;padding:1rem;border:1px solid #e5e7eb;"
                f"border-radius:12px;'><strong>Producto destacado: {data['product']}</strong>"
                f"<br><a href='{data['amazon']}' target='_blank' rel='nofollow sponsored noopener' "
                f"class='btn btn-primary' style='margin-top:.75rem;'>Ver {data['product']} en Amazon →</a></div>"
            )
            post.content = post.content.replace(marker, marker + card, 1)
            post.save(update_fields=["content", "updated_at"])


def reverse_replace_images(apps, schema_editor):
    pass


class Migration(migrations.Migration):
    dependencies = [("blog", "0025_eliminar_imagen_cabecera_duplicada")]
    operations = [migrations.RunPython(replace_images, reverse_replace_images)]
