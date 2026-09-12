from django.db import migrations

POST_SLUG = "viajar-camper-invierno"
MARKER = "recomendaciones-invierno-monetizacion"


def reforzar_invierno(apps, schema_editor):
    Post = apps.get_model("blog", "Post")
    post = Post.objects.filter(slug=POST_SLUG).first()
    if not post or MARKER in (post.content or ""):
        return

    bloque = f'''
<div id="{MARKER}">
<h2>Qué comprar primero para preparar una camper para el invierno</h2>
<p>No hace falta llenar la camper de accesorios. Para una escapada invernal compensa priorizar primero el aislamiento, después el control de la humedad y, por último, los elementos de confort.</p>
<ol>
<li><strong>Oscurecedores térmicos:</strong> son una de las mejoras más sencillas para limitar pérdidas de calor por cristales y cabina.</li>
<li><strong>Termómetro e higrómetro:</strong> permiten vigilar temperatura y humedad para saber cuándo conviene ventilar.</li>
<li><strong>Ropa de cama y manta adecuadas:</strong> mejoran el confort nocturno sin depender únicamente de aumentar la calefacción.</li>
<li><strong>Organización y cocina:</strong> mantener el interior despejado y poder preparar algo caliente resulta especialmente útil cuando se pasa más tiempo dentro del vehículo.</li>
</ol>
<p><strong>Importante con la calefacción:</strong> utiliza únicamente sistemas aptos para vehículos o espacios cerrados según las instrucciones del fabricante. No improvises con hornillos, braseros u otros aparatos de combustión para calentar el habitáculo.</p>
<p>Para completar el equipo puedes consultar nuestra <a href="/shop/"><strong>selección de accesorios camper y camping →</strong></a>. También te pueden interesar nuestras guías sobre <a href="/blog/mejores-aislantes-termicos-camper/"><strong>aislamiento térmico para camper</strong></a> y <a href="/blog/como-mantener-caliente-autocaravana-invierno/"><strong>cómo mantener caliente una autocaravana en invierno</strong></a>.</p>
</div>
'''

    content = post.content or ""
    lower = content.lower()
    candidates = [
        lower.find("<hr>"),
        lower.find("este artículo puede incluir enlaces de afiliado"),
        lower.find("este articulo puede incluir enlaces de afiliado"),
    ]
    positions = [p for p in candidates if p >= 0]
    insert_at = min(positions) if positions else len(content)
    post.content = content[:insert_at] + bloque + content[insert_at:]
    post.save(update_fields=["content"])


class Migration(migrations.Migration):
    dependencies = [
        ("blog", "0068_reforzar_dormir_mejor_camper_monetizacion"),
    ]

    operations = [
        migrations.RunPython(reforzar_invierno, migrations.RunPython.noop),
    ]
