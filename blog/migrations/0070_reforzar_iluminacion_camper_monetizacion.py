from urllib.parse import quote

from django.db import migrations


POST_SLUGS = [
    "como-mejorar-iluminacion-camper",
    "mejorar-iluminacion-camper",
]
MARKER = "recomendaciones-iluminacion-camper-monetizacion"
AWIN_MID = "105405"
AWIN_AFFID = "2917197"
DECATHLON_BL100 = (
    "https://www.decathlon.es/es/p/lampara-de-camping-100-lumenes-ipx4-"
    "pilas-incluidas-quechua-bl100/172514/c98c66m8492468"
)
BL100_DEEP_LINK = (
    f"https://www.awin1.com/cread.php?awinmid={AWIN_MID}&awinaffid={AWIN_AFFID}"
    f"&ued={quote(DECATHLON_BL100, safe='')}"
)
AMAZON_LED = "https://www.amazon.es/s?k=luces+led+12v+camper&tag=caravaning0a-21"
AMAZON_READING = "https://www.amazon.es/s?k=luz+lectura+12v+camper&tag=caravaning0a-21"


def reforzar_iluminacion(apps, schema_editor):
    Post = apps.get_model("blog", "Post")

    post = None
    for slug in POST_SLUGS:
        post = Post.objects.filter(slug=slug).first()
        if post:
            break

    if not post:
        post = Post.objects.filter(title__icontains="iluminación").first()
    if not post:
        post = Post.objects.filter(title__icontains="iluminacion").first()
    if not post or MARKER in (post.content or ""):
        return

    bloque = f'''
<div id="{MARKER}">
<h2>Qué iluminación merece la pena instalar en una camper</h2>
<p>La mejor combinación suele ser sencilla: una iluminación fija de bajo consumo para el interior y una lámpara portátil para mesa, exterior o emergencias. Así evitas llenar la camper de focos y mantienes el consumo eléctrico bajo control.</p>
<ul>
<li><strong>Tiras o plafones LED de 12 V:</strong> son una buena opción para la iluminación general porque consumen poco y pueden integrarse en muebles o techo. <a href="{AMAZON_LED}" target="_blank" rel="nofollow sponsored noopener">Ver opciones LED 12 V en Amazon →</a></li>
<li><strong>Luz de lectura dirigida:</strong> resulta práctica junto a la cama o en la zona de asiento y evita encender toda la iluminación interior. <a href="{AMAZON_READING}" target="_blank" rel="nofollow sponsored noopener">Ver luces de lectura 12 V en Amazon →</a></li>
<li><strong>Lámpara portátil:</strong> para usar dentro y fuera de la camper, una opción sencilla es la <strong>Quechua BL100 de 100 lúmenes</strong>. Funciona con pilas AA y no es recargable. <a href="{BL100_DEEP_LINK}" target="_blank" rel="nofollow sponsored noopener">Ver la Quechua BL100 en Decathlon →</a></li>
</ul>
<p><strong>Consejo:</strong> prioriza luz cálida o neutra en la zona de descanso y reserva una luz más intensa para cocina o tareas. En una camper, iluminar bien no significa iluminarlo todo a la vez.</p>
<p>También puedes encontrar la BL100 y otros accesorios en nuestra <a href="/shop/"><strong>selección de equipamiento camper y camping →</strong></a>.</p>
</div>
'''

    content = post.content or ""
    lower = content.lower()
    candidates = [
        lower.find("<hr>"),
        lower.find("este artículo puede incluir enlaces de afiliado"),
        lower.find("este articulo puede incluir enlaces de afiliado"),
        lower.find("en calidad de afiliado de amazon"),
    ]
    positions = [p for p in candidates if p >= 0]
    insert_at = min(positions) if positions else len(content)

    post.content = content[:insert_at] + bloque + content[insert_at:]
    post.save(update_fields=["content"])


class Migration(migrations.Migration):
    dependencies = [
        ("blog", "0069_reforzar_viajar_camper_invierno_monetizacion"),
    ]

    operations = [
        migrations.RunPython(reforzar_iluminacion, migrations.RunPython.noop),
    ]
