from django.db import migrations


AMAZON_TAG = "caravaning0a-21"


def reforzar_dormir_mejor(apps, schema_editor):
    Post = apps.get_model("blog", "Post")

    post = Post.objects.filter(slug="accesorios-dormir-mejor-camper").first()
    if not post:
        return

    marker = "refuerzo-dormir-mejor-camper-0068"
    if marker in (post.content or ""):
        return

    bloque = f'''
<div id="{marker}">
<h2>Qué comprar primero para dormir mejor en una camper</h2>
<p>Si no quieres llenar la camper de accesorios desde el primer viaje, conviene priorizar lo que más impacto tiene en el descanso: comodidad del colchón, oscuridad, temperatura y orden junto a la cama.</p>
<ul>
<li><strong>Topper plegable:</strong> útil cuando el colchón original resulta demasiado firme o tiene uniones incómodas. <a href="https://www.amazon.es/s?k=topper+plegable+camper&tag={AMAZON_TAG}" target="_blank" rel="nofollow sponsored noopener">Ver opciones en Amazon →</a></li>
<li><strong>Oscurecedores térmicos:</strong> ayudan con la luz exterior y también reducen parte del intercambio térmico en ventanas y cabina. <a href="https://www.amazon.es/s?k=oscurecedores+termicos+camper&tag={AMAZON_TAG}" target="_blank" rel="nofollow sponsored noopener">Ver opciones en Amazon →</a></li>
<li><strong>Almohada compacta o viscoelástica:</strong> ocupa menos espacio y puede mejorar bastante el descanso frente a una almohada de viaje demasiado fina. <a href="https://www.amazon.es/s?k=almohada+viscoelastica+compacta+camping&tag={AMAZON_TAG}" target="_blank" rel="nofollow sponsored noopener">Ver opciones en Amazon →</a></li>
<li><strong>Organizador para la cama:</strong> permite tener móvil, gafas, linterna o cargador a mano sin dejar objetos sueltos. <a href="https://www.amazon.es/s?k=organizador+cama+camper&tag={AMAZON_TAG}" target="_blank" rel="nofollow sponsored noopener">Ver opciones en Amazon →</a></li>
</ul>
<p><strong>Consejo de compra:</strong> antes de elegir un topper u oscurecedor, mide exactamente la cama y las ventanas. En una camper, unos centímetros de error convierten una buena compra en un trasto difícil de guardar.</p>
<p><strong>Más equipamiento recomendado:</strong> <a href="/shop/">consulta nuestra selección de accesorios camper y camping →</a></p>
</div>
'''

    content = post.content or ""
    lower = content.lower()
    disclosure_markers = [
        "este artículo puede incluir enlaces de afiliado",
        "este articulo puede incluir enlaces de afiliado",
        "en calidad de afiliado de amazon",
        "aviso de afili",
    ]

    positions = [lower.find(text) for text in disclosure_markers if lower.find(text) >= 0]
    if positions:
        pos = min(positions)
        paragraph_start = content.rfind("<p", 0, pos)
        hr_start = content.rfind("<hr", 0, pos)
        candidates = [x for x in [paragraph_start, hr_start] if x >= 0]
        insert_at = min(candidates) if candidates else pos
        content = content[:insert_at] + bloque + content[insert_at:]
    else:
        content += bloque
        content += '<hr><p><small>Este artículo puede incluir enlaces de afiliado. En calidad de Afiliado de Amazon, obtenemos ingresos por las compras adscritas que cumplen los requisitos aplicables, sin coste adicional para ti.</small></p>'

    post.content = content
    post.save(update_fields=["content"])


class Migration(migrations.Migration):
    dependencies = [
        ("blog", "0067_reforzar_organizacion_autocaravana_monetizacion"),
    ]

    operations = [
        migrations.RunPython(reforzar_dormir_mejor, migrations.RunPython.noop),
    ]
