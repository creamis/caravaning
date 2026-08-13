from django.db import migrations

POST_SLUG = "escapada-fin-de-semana-autocaravana"

CONTENT = """
<h2>Qué llevar para una escapada de fin de semana en autocaravana</h2>
<p>Una escapada de dos o tres días en autocaravana no necesita una lista interminable de equipaje. La clave está en llevar lo necesario para viajar, cocinar, dormir y disfrutar del destino sin llenar todos los armarios.</p>

<h3>1. Documentación y básicos del viaje</h3>
<ul>
<li>Documentación personal y del vehículo.</li>
<li>Seguro y asistencia en carretera.</li>
<li>Tarjetas y algo de efectivo.</li>
<li>Móvil, cargadores y batería externa.</li>
</ul>

<h3>2. Ropa para dos o tres días</h3>
<p>Elige prendas versátiles y adapta la ropa al tiempo previsto. Para una escapada corta suele ser suficiente con varios cambios de ropa, ropa interior, calzado cómodo y una prenda de abrigo aunque viajes en una época cálida.</p>

<h3>3. Comida y bebida</h3>
<p>Planifica las comidas antes de salir. Llevar productos fáciles de conservar y preparar ayuda a ahorrar espacio y evita cargar con alimentos que finalmente no utilizarás.</p>
<ul>
<li>Agua y bebidas.</li>
<li>Desayunos sencillos.</li>
<li>Comida para las principales comidas.</li>
<li>Snacks para el viaje.</li>
<li>Café, té u otras bebidas habituales.</li>
</ul>

<h3>4. Cocina y limpieza</h3>
<p>Comprueba antes de salir que tienes gas o la fuente de energía necesaria para cocinar. También conviene llevar una pequeña cantidad de productos de limpieza, bolsas de basura, papel de cocina y bayetas.</p>

<h3>5. Dormir cómodamente</h3>
<p>Revisa la cama, las sábanas o saco, almohadas y cualquier elemento que utilices habitualmente para descansar. Si viajas en una época fría, comprueba también que el sistema de calefacción funciona antes de salir.</p>

<h3>6. Higiene personal</h3>
<ul>
<li>Neceser básico.</li>
<li>Toallas.</li>
<li>Gel y champú.</li>
<li>Papel higiénico.</li>
<li>Medicamentos de uso habitual.</li>
</ul>

<h3>7. Para disfrutar del destino</h3>
<p>Aquí es donde merece la pena dejar algo de espacio. Una mesa y sillas exteriores, calzado cómodo, cámara, juegos o material deportivo pueden convertir una parada sencilla en una parte importante del viaje.</p>

<h3>8. Una pequeña caja de emergencia</h3>
<p>Para una escapada corta también conviene llevar algunos elementos básicos: linterna, guantes de trabajo, cinta americana, bridas, fusibles adecuados para el vehículo y un pequeño botiquín.</p>

<h3>9. Antes de salir</h3>
<p>Haz una última revisión de agua, gas, batería, combustible, neumáticos, luces y cierres de puertas y ventanas. También comprueba que todo lo que pueda moverse durante la marcha está correctamente guardado.</p>

<h3>Accesorios útiles para una escapada corta</h3>
<ul>
<li><a href="https://www.amazon.es/s?k=organizador+autocaravana+camper&tag=caravaning0a-21" target="_blank" rel="nofollow sponsored noopener">Organizadores para autocaravana y camper</a></li>
<li><a href="https://www.amazon.es/s?k=mesa+plegable+camping+camper&tag=caravaning0a-21" target="_blank" rel="nofollow sponsored noopener">Mesa plegable de camping</a></li>
<li><a href="https://www.amazon.es/s?k=linterna+recargable+camping&tag=caravaning0a-21" target="_blank" rel="nofollow sponsored noopener">Linterna recargable</a></li>
<li><a href="https://www.amazon.es/s?k=botiquin+primeros+auxilios+camping&tag=caravaning0a-21" target="_blank" rel="nofollow sponsored noopener">Botiquín de primeros auxilios</a></li>
</ul>

<p><strong>Consejo final:</strong> para un fin de semana, intenta salir con margen de espacio. Llevar menos cosas pero tenerlas bien organizadas hace que la autocaravana resulte mucho más cómoda durante el viaje.</p>
<hr><p><small>Este artículo puede incluir enlaces de afiliado. En calidad de Afiliado de Amazon, obtenemos ingresos por las compras adscritas que cumplen los requisitos aplicables, sin coste adicional para ti.</small></p>
"""

# Imágenes de Wikimedia Commons seleccionadas por representar directamente
# camper/autocaravana en viaje o entorno de camping. Special:FilePath redirige
# al archivo original de imagen y evita depender de CDNs comerciales inestables.
IMAGES = [
    "https://commons.wikimedia.org/wiki/Special:FilePath/Camper%20van%20with%20family%20inside%20playing%20games.jpg",
    "https://commons.wikimedia.org/wiki/Special:FilePath/New%20Camping%20Area%20at%20the%20Caravan%20and%20Motorhome%20Club%20Site%20-%20geograph.org.uk%20-%208341704.jpg",
    "https://commons.wikimedia.org/wiki/Special:FilePath/Bespoke%20Volkswagen%20campervan%20interior%20built%20by%20The%20Wee%20Camper%20Co..jpg",
]


def create_post(apps, schema_editor):
    Post = apps.get_model("blog", "Post")
    User = apps.get_model("auth", "User")
    PostImage = apps.get_model("blog", "PostImage")

    post = Post.objects.filter(slug=POST_SLUG).first()
    if not post:
        author = User.objects.order_by("id").first()
        if not author:
            return
        post = Post.objects.create(
            slug=POST_SLUG,
            title="Qué llevar para una escapada de fin de semana en autocaravana",
            content=CONTENT,
            meta_description="Qué llevar en una escapada de fin de semana en autocaravana: comida, ropa, cocina, higiene, seguridad y accesorios útiles.",
            status="PUBLISHED",
            author=author,
        )
    else:
        post.content = CONTENT
        post.meta_description = "Qué llevar en una escapada de fin de semana en autocaravana: comida, ropa, cocina, higiene, seguridad y accesorios útiles."
        post.status = "PUBLISHED"
        post.save(update_fields=["content", "meta_description", "status"])

    PostImage.objects.filter(post=post).delete()
    for url in IMAGES:
        PostImage.objects.create(post=post, image_url=url)


class Migration(migrations.Migration):
    dependencies = [("blog", "0054_imagenes_iluminacion_camper_reales")]
    operations = [migrations.RunPython(create_post, migrations.RunPython.noop)]
