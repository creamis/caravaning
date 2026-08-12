from django.db import migrations

POST_SLUG = "20-accesorios-imprescindibles-camper-menos-50-euros"
TAG = "caravaning0a-21"

PRODUCTS = [
    ("Cargador USB-C para varios dispositivos", "cargador USB C coche camping", "https://images.unsplash.com/photo-1609592424696-b4e7a6e6f6b5?auto=format&fit=crop&w=1400&q=80"),
    ("Power bank de gran capacidad", "power bank 20000mah camping", "https://images.unsplash.com/photo-1609592424696-b4e7a6e6f6b5?auto=format&fit=crop&w=1400&q=80"),
    ("Lámpara LED recargable", "lampara LED camping recargable", "https://images.unsplash.com/photo-1507473885765-e6ed057f782c?auto=format&fit=crop&w=1400&q=80"),
    ("Ventilador portátil recargable", "ventilador camping recargable", "https://images.unsplash.com/photo-1592489936268-6e3a6c7b3c7d?auto=format&fit=crop&w=1400&q=80"),
    ("Lámpara antimosquitos", "lampara antimosquitos USB camping", "https://images.unsplash.com/photo-1507525428034-b723cf961d3e?auto=format&fit=crop&w=1400&q=80"),
    ("Mini aspirador portátil", "mini aspirador portatil coche", "https://images.unsplash.com/photo-1558317374-067fb5f30001?auto=format&fit=crop&w=1400&q=80"),
    ("Papelera plegable", "papelera plegable camping", "https://images.unsplash.com/photo-1528323273322-d81458248d40?auto=format&fit=crop&w=1400&q=80"),
    ("Organizadores de almacenamiento", "organizadores camper autocaravana", "https://images.unsplash.com/photo-1556911220-e15b29be8c8f?auto=format&fit=crop&w=1400&q=80"),
    ("Organizador para zapatos", "organizador zapatos camping camper", "https://images.unsplash.com/photo-1542291026-7eec264c27ff?auto=format&fit=crop&w=1400&q=80"),
    ("Set de cocina compacto", "set cocina camping compacto", "https://images.unsplash.com/photo-1556910103-1c02745aae4d?auto=format&fit=crop&w=1400&q=80"),
    ("Cafetera portátil", "cafetera portatil camping", "https://images.unsplash.com/photo-1495474472287-4d71bcdd2085?auto=format&fit=crop&w=1400&q=80"),
    ("Botellas reutilizables", "botellas reutilizables camping", "https://images.unsplash.com/photo-1602143407151-7111542de6e8?auto=format&fit=crop&w=1400&q=80"),
    ("Ducha portátil", "ducha portatil camping", "https://images.unsplash.com/photo-1502744688674-c619d1586c9e?auto=format&fit=crop&w=1400&q=80"),
    ("Mesa auxiliar plegable", "mesa plegable camping", "https://images.unsplash.com/photo-1505693416388-ac5ce068fe85?auto=format&fit=crop&w=1400&q=80"),
    ("Ganchos y organizadores", "ganchos organizadores camper", "https://images.unsplash.com/photo-1586023492125-27b2c045efd7?auto=format&fit=crop&w=1400&q=80"),
    ("Tendedero portátil", "tendedero portatil camping", "https://images.unsplash.com/photo-1604335399105-a0c585fd81a1?auto=format&fit=crop&w=1400&q=80"),
    ("Detector de humo y monóxido de carbono", "detector monoxido carbono humo camping", "https://images.unsplash.com/photo-1558008258-3256797b43f3?auto=format&fit=crop&w=1400&q=80"),
    ("Kit compacto de herramientas", "kit herramientas coche camping", "https://images.unsplash.com/photo-1581147036324-c17ac41a76f7?auto=format&fit=crop&w=1400&q=80"),
    ("Linterna LED", "linterna LED camping recargable", "https://images.unsplash.com/photo-1510133769060-4c4c1f3f5f5a?auto=format&fit=crop&w=1400&q=80"),
    ("Kit de reparación para camping", "kit reparacion camping", "https://images.unsplash.com/photo-1609205807107-e8ec2120f9de?auto=format&fit=crop&w=1400&q=80"),
]

DESCRIPTIONS = [
    "Un cargador multipuerto permite cargar móvil, tablet, reloj o cámara desde un único punto. En una camper, donde cada enchufe cuenta, es uno de esos accesorios que se utilizan prácticamente a diario.",
    "Una batería externa es una red de seguridad para excursiones, playas, rutas de senderismo o noches en las que no quieres depender de la instalación eléctrica del vehículo.",
    "Una lámpara LED independiente resulta útil dentro y fuera de la camper. Busca modelos recargables y con varias intensidades para utilizarla como luz ambiente o de trabajo.",
    "Durante las noches calurosas puede marcar una gran diferencia. Un modelo con batería, varias velocidades y funcionamiento silencioso resulta especialmente práctico.",
    "Para disfrutar del exterior al anochecer sin convertir la cena en un buffet de insectos, una lámpara antimosquitos puede ser un accesorio práctico.",
    "Arena, migas y tierra entran en una camper con una facilidad casi científica. Un aspirador compacto permite mantener limpio el interior sin sacar un equipo grande.",
    "Una papelera compacta ayuda a mantener ordenada la zona de cocina y puede plegarse cuando no se utiliza.",
    "Cajas y bolsas organizadoras permiten aprovechar mejor armarios y huecos. En una camper, ordenar bien significa también encontrar las cosas a la primera.",
    "Un organizador específico evita que el calzado termine ocupando el suelo y facilita separar botas, chanclas y zapatillas.",
    "Un conjunto compacto de utensilios puede ahorrar espacio y evitar llevar media cocina de casa. Prioriza piezas apilables y fáciles de limpiar.",
    "Para muchos viajeros, el café de la mañana forma parte del ritual. Una cafetera compacta permite prepararlo sin ocupar demasiado espacio.",
    "Las botellas reutilizables reducen residuos y facilitan tener agua a mano durante las rutas y excursiones.",
    "Una ducha portátil puede resultar muy útil después de la playa, una ruta de montaña o una jornada de bicicleta, especialmente cuando el vehículo no dispone de ducha.",
    "Una mesa ligera y plegable amplía el espacio exterior y puede convertirse en zona para comer, cocinar o apoyar el portátil.",
    "Los ganchos y soluciones de organización permiten aprovechar paredes, puertas y pequeños espacios para colgar toallas, utensilios o accesorios.",
    "Un tendedero compacto permite secar bañadores, toallas y ropa después de una jornada de playa o piscina sin ocupar demasiado espacio.",
    "No es el accesorio más divertido de la lista, pero sí uno de los más importantes. Un detector adecuado aporta una capa adicional de seguridad. Comprueba siempre que sea apropiado para el uso que vas a darle.",
    "Un pequeño juego de herramientas puede resolver ajustes y reparaciones sencillas durante el viaje. Conviene adaptarlo al vehículo y no sustituye una revisión profesional cuando existe una avería importante.",
    "Aunque llevemos el móvil, una linterna independiente sigue siendo muy útil para revisar el exterior, buscar algo por la noche o solucionar una incidencia.",
    "Un pequeño kit de reparación puede salvar una salida cuando aparece un problema menor. La composición ideal depende del tipo de camper y del equipamiento que lleves.",
]


def build_post(apps, schema_editor):
    Post = apps.get_model("blog", "Post")
    PostImage = apps.get_model("blog", "PostImage")
    User = apps.get_model("auth", "User")

    author = User.objects.filter(username="miguel").first() or User.objects.filter(is_superuser=True).first()
    if not author:
        return

    post = Post.objects.filter(slug=POST_SLUG).first()
    if not post:
        post = Post.objects.create(
            author=author,
            title="Los 20 accesorios imprescindibles para una camper por menos de 50 €",
            slug=POST_SLUG,
            meta_description="Descubre 20 accesorios imprescindibles para camper por menos de 50 €. Organización, cocina, iluminación, energía y comodidad para viajar mejor sin gastar una fortuna.",
            content="",
            status="PUBLISHED",
        )
    else:
        post.author = author
        post.title = "Los 20 accesorios imprescindibles para una camper por menos de 50 €"
        post.meta_description = "Descubre 20 accesorios imprescindibles para camper por menos de 50 €. Organización, cocina, iluminación, energía y comodidad para viajar mejor sin gastar una fortuna."
        post.status = "PUBLISHED"

    cover = "https://images.unsplash.com/photo-1523987355523-c7b5b0dd90a7?auto=format&fit=crop&w=1600&q=85"
    PostImage.objects.get_or_create(post=post, image_url=cover)

    body = """
<p><strong>Viajar en camper no significa tener que gastar una fortuna para estar cómodo.</strong> Hay accesorios pequeños, baratos y sorprendentemente útiles que pueden hacer que una escapada sea mucho más práctica.</p>
<p>Hemos reunido <strong>20 accesorios imprescindibles para camper por menos de 50 €</strong> que pueden ayudarte con la organización, la iluminación, la cocina, la energía, la limpieza y el día a día.</p>
<div style="margin:24px 0;padding:18px;border-radius:16px;background:#f5f5f5;"><strong>💡 Consejo:</strong> no necesitas comprar los 20. Elige los que solucionen problemas reales de tu forma de viajar.</div>
"""

    for i, ((name, query, image_url), description) in enumerate(zip(PRODUCTS, DESCRIPTIONS), start=1):
        amazon_url = "https://www.amazon.es/s?k=" + query.replace(" ", "+") + "&tag=" + TAG
        body += f'<h2>{i}. {name}</h2>'
        body += f'<p>{description}</p>'
        body += f'<img src="{image_url}" alt="{name}" loading="lazy" style="width:100%;aspect-ratio:16/9;height:auto;object-fit:cover;border-radius:16px;margin:20px 0;">'
        body += '<p><strong>💶 Precio orientativo:</strong> menos de 50 €.</p>'
        body += f'<p><a href="{amazon_url}" target="_blank" rel="nofollow sponsored noopener" style="display:inline-block;padding:12px 18px;border-radius:10px;background:#ff9900;color:#111;text-decoration:none;font-weight:700;">🛒 Ver opciones de {name.lower()} en Amazon</a></p>'

    body += """
<div style="margin:30px 0;padding:16px;border:1px solid #ddd;border-radius:12px;"><strong>Nota de afiliación:</strong> Algunos enlaces de este artículo son enlaces de afiliado. Si realizas una compra después de acceder a ellos, Caravaning Project puede recibir una comisión sin que esto suponga un coste adicional para ti. Los precios y la disponibilidad pueden cambiar.</div>
<h2>¿Realmente necesitas los 20 accesorios?</h2>
<p>No. El mejor equipamiento camper es el que resuelve un problema concreto sin llenar todos los armarios. Si estás empezando, prioriza iluminación, energía, organización, seguridad y los accesorios relacionados con las actividades que realizas habitualmente.</p>
<h2>Conclusión</h2>
<p>Preparar una camper puede convertirse fácilmente en una colección infinita de accesorios. Con un presupuesto moderado, sin embargo, puedes conseguir mejoras muy útiles para viajar con más comodidad y organización.</p>
<p><strong>¿Cuál de estos accesorios llevas siempre en tu camper?</strong> Cuéntanoslo y ampliaremos la lista con nuevas ideas.</p>
"""

    post.content = body
    post.save()

    for name, query, image_url in PRODUCTS:
        PostImage.objects.get_or_create(post=post, image_url=image_url)


def reverse_build_post(apps, schema_editor):
    pass


class Migration(migrations.Migration):
    dependencies = [("blog", "0015_add_amazon_affiliate_links")]
    operations = [migrations.RunPython(build_post, reverse_build_post)]
