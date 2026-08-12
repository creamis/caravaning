from django.db import migrations

GUIDES = {
    "tpms-caravana-autocaravana-monitor-presion-neumaticos": {
        "image": "https://commons.wikimedia.org/wiki/Special:Redirect/file/Tire_pressure_sensors.jpg",
        "credit": "Tire pressure sensors, TpmsReset, CC BY-SA 4.0, Wikimedia Commons",
        "links": [
            ("TPMS para caravana de 4 sensores", "https://www.amazon.es/s?k=TPMS+caravana+4+sensores&tag=caravaning0a-21"),
            ("TPMS para caravana de 6 sensores", "https://www.amazon.es/s?k=TPMS+caravana+6+sensores&tag=caravaning0a-21"),
            ("TPMS con presión y temperatura", "https://www.amazon.es/s?k=TPMS+presion+temperatura+caravana&tag=caravaning0a-21"),
            ("Sensores TPMS para remolque", "https://www.amazon.es/s?k=sensores+TPMS+remolque+caravana&tag=caravaning0a-21"),
        ],
    },
    "como-nivelar-caravana-calzos-rampas-nivel": {
        "image": "https://commons.wikimedia.org/wiki/Special:Redirect/file/Hopton_-_caravan_-_Outdoors_-_ramp_-_patio_-_exterior_-_2020.jpg",
        "credit": "Hopton - caravan - Outdoors - ramp - patio - exterior - 2020, RainbowCrt, Wikimedia Commons",
        "links": [
            ("Rampas niveladoras para caravana", "https://www.amazon.es/s?k=rampas+niveladoras+caravana&tag=caravaning0a-21"),
            ("Calzos para ruedas de caravana", "https://www.amazon.es/s?k=calzos+ruedas+caravana&tag=caravaning0a-21"),
            ("Nivel de burbuja para caravana", "https://www.amazon.es/s?k=nivel+burbuja+caravana&tag=caravaning0a-21"),
            ("Placas de apoyo para patas", "https://www.amazon.es/s?k=placas+apoyo+patas+caravana&tag=caravaning0a-21"),
        ],
    },
    "agua-caravana-depositos-bombas-bidones-accesorios": {
        "image": "https://commons.wikimedia.org/wiki/Special:Redirect/file/SAT_Grinda_camping_vattenpump.jpg",
        "credit": "SAT Grinda camping vattenpump, Salgo60, CC0, Wikimedia Commons",
        "links": [
            ("Manguera para agua potable de camping", "https://www.amazon.es/s?k=manguera+agua+potable+camping+caravana&tag=caravaning0a-21"),
            ("Bidón de agua potable", "https://www.amazon.es/s?k=bidon+agua+potable+camping&tag=caravaning0a-21"),
            ("Bomba de agua 12V para caravana", "https://www.amazon.es/s?k=bomba+agua+12v+caravana&tag=caravaning0a-21"),
            ("Filtro de agua para caravana", "https://www.amazon.es/s?k=filtro+agua+caravana+camper&tag=caravaning0a-21"),
        ],
    },
    "wc-portatil-camping-camper-caravana-guia-compra": {
        "image": "https://commons.wikimedia.org/wiki/Special:Redirect/file/Foldable_camping_UDD_toilet_by_Separett_%28Sweden%29_%282921708370%29.jpg",
        "credit": "Foldable camping UDD toilet by Separett, SuSanA Secretariat, CC BY 2.0, Wikimedia Commons",
        "links": [
            ("WC químico portátil para camping", "https://www.amazon.es/s?k=wc+quimico+portatil+camping&tag=caravaning0a-21"),
            ("WC portátil para caravana", "https://www.amazon.es/s?k=wc+portatil+caravana&tag=caravaning0a-21"),
            ("Productos para WC químico", "https://www.amazon.es/s?k=producto+wc+quimico+camping&tag=caravaning0a-21"),
            ("Tienda de privacidad para WC", "https://www.amazon.es/s?k=tienda+privacidad+wc+camping&tag=caravaning0a-21"),
        ],
    },
    "toldo-avance-caravana-guia-compra": {
        "image": "https://commons.wikimedia.org/wiki/Special:Redirect/file/Wohnwagen-vorzelt.jpg",
        "credit": "Wohnwagen-vorzelt.jpg, Lena Middendorf, CC BY-SA 4.0, Wikimedia Commons",
        "links": [
            ("Toldos para caravana", "https://www.amazon.es/s?k=toldo+caravana&tag=caravaning0a-21"),
            ("Avances para caravana", "https://www.amazon.es/s?k=avance+caravana&tag=caravaning0a-21"),
            ("Cerramientos para toldo", "https://www.amazon.es/s?k=cerramiento+toldo+caravana&tag=caravaning0a-21"),
            ("Accesorios para toldos y avances", "https://www.amazon.es/s?k=accesorios+toldo+avance+caravana&tag=caravaning0a-21"),
        ],
    },
}


def update_guides(apps, schema_editor):
    Post = apps.get_model("blog", "Post")
    PostImage = apps.get_model("blog", "PostImage")

    old_markers = [
        "<p><strong>🛒 Consulta modelos de TPMS para caravana y autocaravana en Amazon</strong></p>",
        "<p><strong>🛒 Ver rampas, calzos y niveles para caravanas en Amazon</strong></p>",
        "<p><strong>🛒 Ver accesorios para agua de caravanas y autocaravanas en Amazon</strong></p>",
        "<p><strong>🛒 Ver WC portátiles y accesorios de camping en Amazon</strong></p>",
        "<p><strong>🛒 Ver toldos, avances y cerramientos para caravanas en Amazon</strong></p>",
    ]

    for slug, data in GUIDES.items():
        post = Post.objects.filter(slug=slug).first()
        if not post:
            continue

        text = post.content
        for marker in old_markers:
            text = text.replace(marker, "")

        image_html = (
            f"<figure style='margin:0 0 1.5rem 0;text-align:center;'>"
            f"<img src='{data['image']}' loading='lazy' style='max-width:100%;height:auto;border-radius:12px;' alt='{post.title}'>"
            f"<figcaption style='font-size:.85rem;color:#666;margin-top:.5rem;'>Imagen ilustrativa. {data['credit']}.</figcaption>"
            f"</figure>"
        )

        links_html = "<section><h2>🛒 Productos que puedes consultar en Amazon</h2><p>Estas búsquedas te llevan directamente a Amazon para comparar modelos, precios y disponibilidad. Los precios pueden cambiar.</p>"
        for name, url in data["links"]:
            links_html += f"<p><a href='{url}' target='_blank' rel='nofollow sponsored noopener' class='btn btn-primary'>Ver {name} en Amazon →</a></p>"
        links_html += "</section>"

        if data["image"] not in text:
            text = image_html + text
        if "Productos que puedes consultar en Amazon" not in text:
            text = text.replace("<hr>", links_html + "<hr>", 1)

        post.content = text
        post.save(update_fields=["content", "updated_at"])

        PostImage.objects.filter(post=post).delete()
        PostImage.objects.create(post=post, image_url=data["image"])


def reverse_update_guides(apps, schema_editor):
    pass


class Migration(migrations.Migration):
    dependencies = [("blog", "0022_guias_compra_caravaning")]
    operations = [migrations.RunPython(update_guides, reverse_update_guides)]
