from django.db import migrations


AMAZON_TAG = "caravaning0a-21"


def amazon_search(query):
    from urllib.parse import quote_plus
    return f"https://www.amazon.es/s?k={quote_plus(query)}&tag={AMAZON_TAG}"


def reforzar_cocina_camper(apps, schema_editor):
    Post = apps.get_model("blog", "Post")

    post = Post.objects.filter(slug="que-llevar-para-cocinar-en-una-camper-pequena").first()
    if not post:
        post = Post.objects.filter(title__icontains="cocinar en una camper").first()
    if not post:
        return

    marker = "recomendaciones-cocina-camper-monetizacion"
    if marker in post.content:
        return

    bloque = f'''
<div id="{marker}">
<h2>Accesorios prácticos para cocinar en una camper pequeña</h2>
<p>En una cocina camper cada centímetro cuenta. Antes de comprar más utensilios conviene priorizar piezas compactas, plegables y que puedan cumplir varias funciones.</p>
<ul>
<li><strong>Menaje apilable:</strong> ayuda a aprovechar armarios pequeños y evita llevar cazos y sartenes de más. <a href="{amazon_search('menaje apilable camper camping')}" target="_blank" rel="nofollow sponsored noopener">Ver opciones en Amazon →</a></li>
<li><strong>Utensilios plegables:</strong> escurridores, recipientes y accesorios de silicona reducen mucho el volumen cuando no se utilizan. <a href="{amazon_search('utensilios cocina plegables camping camper')}" target="_blank" rel="nofollow sponsored noopener">Ver opciones en Amazon →</a></li>
<li><strong>Organizadores para cocina:</strong> útiles para mantener especias, cubiertos y pequeños accesorios sujetos durante el viaje. <a href="{amazon_search('organizador cocina camper autocaravana')}" target="_blank" rel="nofollow sponsored noopener">Ver opciones en Amazon →</a></li>
</ul>
<p><strong>También puedes consultar nuestra selección de equipamiento camper y camping:</strong> <a href="/shop/">ver productos recomendados en la tienda →</a></p>
</div>
'''

    content = post.content or ""
    lower = content.lower()
    disclosure_positions = [
        lower.find("como afiliado"),
        lower.find("enlaces de afiliado"),
        lower.find("enlaces afiliados"),
        lower.find("aviso de afili"),
    ]
    positions = [p for p in disclosure_positions if p >= 0]

    if positions:
        pos = min(positions)
        paragraph_start = content.rfind("<p", 0, pos)
        insert_at = paragraph_start if paragraph_start >= 0 else pos
        content = content[:insert_at] + bloque + content[insert_at:]
    else:
        content += bloque
        content += '<p><small>Este artículo contiene enlaces de afiliado. Si compras a través de ellos, podemos recibir una comisión sin coste adicional para ti.</small></p>'

    post.content = content
    post.save(update_fields=["content"])


class Migration(migrations.Migration):
    dependencies = [
        ("blog", "0065_reforzar_ropa_caravaning_decathlon"),
    ]

    operations = [
        migrations.RunPython(reforzar_cocina_camper, migrations.RunPython.noop),
    ]
