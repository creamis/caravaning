from django.db import migrations
from urllib.parse import quote_plus


AMAZON_TAG = "caravaning0a-21"


def amazon_search(query):
    return f"https://www.amazon.es/s?k={quote_plus(query)}&tag={AMAZON_TAG}"


def reforzar_organizacion(apps, schema_editor):
    Post = apps.get_model("blog", "Post")

    post = Post.objects.filter(slug="como-organizar-una-autocaravana-con-poco-espacio").first()
    if not post:
        post = Post.objects.filter(title__icontains="organizar una autocaravana").first()
    if not post:
        post = Post.objects.filter(title__icontains="poco espacio").first()
    if not post:
        return

    marker = "recomendaciones-organizacion-autocaravana-monetizacion"
    content = post.content or ""
    if marker in content:
        return

    bloque = f'''
<div id="{marker}">
<h2>Accesorios que ayudan a aprovechar mejor el espacio</h2>
<p>No hace falta llenar la autocaravana de gadgets. Los accesorios que más sentido tienen son los que permiten usar mejor huecos que normalmente se desperdician y, además, mantienen todo sujeto durante la marcha.</p>
<ul>
<li><strong>Organizadores colgantes:</strong> prácticos para puertas, laterales de armarios y zonas verticales. <a href="{amazon_search('organizador colgante autocaravana camper')}" target="_blank" rel="nofollow sponsored noopener">Ver opciones en Amazon →</a></li>
<li><strong>Cajas plegables y apilables:</strong> permiten guardar ropa, comida o accesorios y reducir su volumen cuando están vacías. <a href="{amazon_search('cajas plegables camping autocaravana')}" target="_blank" rel="nofollow sponsored noopener">Ver opciones en Amazon →</a></li>
<li><strong>Redes y bolsillos de almacenamiento:</strong> son útiles para aprovechar paredes y evitar que pequeños objetos se desplacen al conducir. <a href="{amazon_search('red almacenamiento camper autocaravana')}" target="_blank" rel="nofollow sponsored noopener">Ver opciones en Amazon →</a></li>
<li><strong>Ganchos y soportes adhesivos:</strong> una solución sencilla para chaquetas, llaves, paños y accesorios ligeros. <a href="{amazon_search('ganchos adhesivos camper autocaravana')}" target="_blank" rel="nofollow sponsored noopener">Ver opciones en Amazon →</a></li>
</ul>
<p><strong>Más ideas de equipamiento:</strong> en nuestra <a href="/shop/">selección de accesorios camper y camping</a> reunimos productos útiles para viajes y organización.</p>
</div>
'''

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
        ("blog", "0066_reforzar_cocinar_camper_monetizacion"),
    ]

    operations = [
        migrations.RunPython(reforzar_organizacion, migrations.RunPython.noop),
    ]
