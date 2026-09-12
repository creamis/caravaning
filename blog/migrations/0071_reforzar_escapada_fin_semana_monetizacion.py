from django.db import migrations

POST_SLUG = "escapada-fin-de-semana-autocaravana"
MARKER = "checklist-escapada-fin-semana-monetizacion"


def reforzar_escapada(apps, schema_editor):
    Post = apps.get_model("blog", "Post")
    post = Post.objects.filter(slug=POST_SLUG).first()
    if not post or MARKER in (post.content or ""):
        return

    bloque = f'''
<div id="{MARKER}">
<h2>Checklist rápida antes de salir</h2>
<p>Para una escapada de dos o tres días, la mejor compra no siempre es llevar más cosas, sino elegir accesorios que resuelvan varios problemas a la vez y ocupen poco espacio.</p>
<ul>
<li><strong>Organización:</strong> cajas, bolsas o pequeños organizadores para que nada viaje suelto.</li>
<li><strong>Exterior:</strong> mesa y sillas plegables si vas a comer o descansar fuera de la autocaravana.</li>
<li><strong>Iluminación:</strong> una lámpara portátil resulta útil tanto dentro como fuera del vehículo.</li>
<li><strong>Seguridad:</strong> botiquín, linterna, guantes y herramientas básicas para pequeños imprevistos.</li>
<li><strong>Energía:</strong> cargadores y una batería externa para móvil y pequeños dispositivos.</li>
</ul>
<p>Si estás preparando el equipo desde cero, puedes ver nuestra <a href="/shop/"><strong>selección de accesorios camper y camping →</strong></a>. También te puede ayudar la guía de <a href="/blog/como-organizar-autocaravana-poco-espacio/"><strong>organización en una autocaravana con poco espacio</strong></a> y el artículo sobre <a href="/blog/como-mejorar-iluminacion-camper/"><strong>cómo mejorar la iluminación de una camper</strong></a>.</p>
<p><strong>Regla útil:</strong> si un objeto no resuelve una necesidad concreta durante el fin de semana, probablemente puede quedarse en casa.</p>
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
        ("blog", "0070_reforzar_iluminacion_camper_monetizacion"),
    ]

    operations = [
        migrations.RunPython(reforzar_escapada, migrations.RunPython.noop),
    ]
