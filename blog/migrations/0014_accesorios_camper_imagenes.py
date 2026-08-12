from django.db import migrations


POST_SLUG = "20-accesorios-imprescindibles-camper-menos-50-euros"

PRODUCTS = [
    ("cargador-usb-c", "https://images.unsplash.com/photo-1609592424696-b4e7a6e6f6b5?auto=format&fit=crop&w=1200&q=80", "Cargador USB-C para varios dispositivos en una camper"),
    ("power-bank", "https://images.unsplash.com/photo-1609592424696-b4e7a6e6f6b5?auto=format&fit=crop&w=1200&q=80", "Batería externa para cargar dispositivos durante un viaje en camper"),
    ("lampara-led", "https://images.unsplash.com/photo-1507473885765-e6ed057f782c?auto=format&fit=crop&w=1200&q=80", "Lámpara LED para iluminar el interior de una camper"),
    ("ventilador-portatil", "https://images.unsplash.com/photo-1592489936268-6e3a6c7b3c7d?auto=format&fit=crop&w=1200&q=80", "Ventilador portátil recargable para camper"),
    ("lampara-antimosquitos", "https://images.unsplash.com/photo-1507525428034-b723cf961d3e?auto=format&fit=crop&w=1200&q=80", "Lámpara antimosquitos para usar en exteriores"),
    ("mini-aspirador", "https://images.unsplash.com/photo-1558317374-067fb5f30001?auto=format&fit=crop&w=1200&q=80", "Mini aspirador portátil para limpiar una camper"),
    ("papelera-plegable", "https://images.unsplash.com/photo-1528323273322-d81458248d40?auto=format&fit=crop&w=1200&q=80", "Papelera compacta para organizar una camper"),
    ("organizadores", "https://images.unsplash.com/photo-1556911220-e15b29be8c8f?auto=format&fit=crop&w=1200&q=80", "Organizadores para aprovechar el espacio de una camper"),
    ("organizador-zapatos", "https://images.unsplash.com/photo-1542291026-7eec264c27ff?auto=format&fit=crop&w=1200&q=80", "Organizador de zapatos para camper"),
    ("set-cocina", "https://images.unsplash.com/photo-1556910103-1c02745aae4d?auto=format&fit=crop&w=1200&q=80", "Utensilios y menaje compacto para cocinar en camper"),
    ("cafetera-portatil", "https://images.unsplash.com/photo-1495474472287-4d71bcdd2085?auto=format&fit=crop&w=1200&q=80", "Cafetera portátil para preparar café durante un viaje"),
    ("botellas", "https://images.unsplash.com/photo-1602143407151-7111542de6e8?auto=format&fit=crop&w=1200&q=80", "Botellas reutilizables para viajar en camper"),
    ("ducha-portatil", "https://images.unsplash.com/photo-1502744688674-c619d1586c9e?auto=format&fit=crop&w=1200&q=80", "Ducha portátil para camping y viajes en camper"),
    ("mesa-plegable", "https://images.unsplash.com/photo-1505693416388-ac5ce068fe85?auto=format&fit=crop&w=1200&q=80", "Mesa auxiliar plegable para camping"),
    ("ganchos", "https://images.unsplash.com/photo-1586023492125-27b2c045efd7?auto=format&fit=crop&w=1200&q=80", "Ganchos y soluciones para organizar una camper"),
    ("tendedero", "https://images.unsplash.com/photo-1604335399105-a0c585fd81a1?auto=format&fit=crop&w=1200&q=80", "Tendedero portátil para viajes en camper"),
    ("detector-co", "https://images.unsplash.com/photo-1558008258-3256797b43f3?auto=format&fit=crop&w=1200&q=80", "Detector de humo y monóxido de carbono para una camper"),
    ("kit-herramientas", "https://images.unsplash.com/photo-1581147036324-c17ac41a76f7?auto=format&fit=crop&w=1200&q=80", "Kit compacto de herramientas para una camper"),
    ("linterna", "https://images.unsplash.com/photo-1510133769060-4c4c1f3f5f5a?auto=format&fit=crop&w=1200&q=80", "Linterna LED para camping y viajes en autocaravana"),
    ("kit-reparacion", "https://images.unsplash.com/photo-1609205807107-e8ec2120f9de?auto=format&fit=crop&w=1200&q=80", "Kit de reparación y mantenimiento para camping"),
]


def add_camper_products(apps, schema_editor):
    Post = apps.get_model("blog", "Post")
    PostImage = apps.get_model("blog", "PostImage")

    post, created = Post.objects.get_or_create(
        slug=POST_SLUG,
        defaults={
            "title": "Los 20 accesorios imprescindibles para una camper por menos de 50 €",
            "meta_description": "Descubre 20 accesorios imprescindibles para camper por menos de 50 €. Organización, cocina, iluminación, energía y comodidad para viajar mejor sin gastar una fortuna.",
            "status": "PUBLISHED",
        },
    )

    if not post.title:
        post.title = "Los 20 accesorios imprescindibles para una camper por menos de 50 €"
    post.status = "PUBLISHED"

    # Imagen de portada
    cover_url = "https://images.unsplash.com/photo-1523987355523-c7b5b0dd90a7?auto=format&fit=crop&w=1600&q=85"
    PostImage.objects.get_or_create(post=post, image_url=cover_url, defaults={"alt_text": "Camper preparada para un viaje por carretera"})

    for slug, image_url, alt_text in PRODUCTS:
        PostImage.objects.get_or_create(post=post, image_url=image_url, defaults={"alt_text": alt_text})

    intro = """
<p><strong>Viajar en camper no significa tener que gastar una fortuna para estar cómodo.</strong> Hay accesorios pequeños, baratos y sorprendentemente útiles que pueden hacer que una escapada sea mucho más práctica.</p>
<p>Hemos reunido <strong>20 accesorios para camper por menos de 50 €</strong> que pueden ayudarte con la organización, la iluminación, la cocina, la energía, la limpieza y el día a día. Los precios de Amazon pueden cambiar, por lo que conviene comprobar el precio actual antes de comprar.</p>
"""
    sections = [
        ("1. Cargador USB-C para varios dispositivos", "Un buen cargador multipuerto permite cargar móvil, tablet, reloj o cámara desde un único punto. En una camper, donde cada enchufe cuenta, es uno de esos accesorios pequeños que terminan utilizándose todos los días.", "cargador-usb-c"),
        ("2. Power bank de gran capacidad", "Una batería externa es una red de seguridad para excursiones, playas, rutas de senderismo o noches en las que no quieres depender de la instalación eléctrica del vehículo.", "power-bank"),
        ("3. Lámpara LED recargable", "Una lámpara LED independiente resulta muy útil dentro y fuera de la camper. Busca modelos recargables y con varias intensidades para poder utilizarla tanto como luz ambiente como iluminación de trabajo.", "lampara-led"),
        ("4. Ventilador portátil recargable", "Durante las noches calurosas puede marcar una gran diferencia. Un modelo con batería, varias velocidades y funcionamiento silencioso es especialmente interesante para una camper.", "ventilador-portatil"),
        ("5. Lámpara antimosquitos", "Para disfrutar del exterior al anochecer sin convertir la cena en un buffet de insectos, una lámpara antimosquitos puede ser un accesorio práctico.", "lampara-antimosquitos"),
        ("6. Mini aspirador portátil", "Arena, migas y tierra entran en una camper con una facilidad casi científica. Un aspirador compacto permite mantener limpio el interior sin sacar un equipo grande.", "mini-aspirador"),
        ("7. Papelera plegable", "Una papelera compacta ayuda a mantener ordenada la zona de cocina y puede plegarse cuando no se utiliza.", "papelera-plegable"),
        ("8. Organizadores de almacenamiento", "Cajas y bolsas organizadoras permiten aprovechar mejor armarios y huecos. En una camper, ordenar bien significa también encontrar las cosas a la primera.", "organizadores"),
        ("9. Organizador para zapatos", "Un organizador específico evita que el calzado termine ocupando el suelo y facilita separar zapatos de montaña, chanclas y zapatillas.", "organizador-zapatos"),
        ("10. Set de cocina compacto", "Un pequeño conjunto de utensilios puede ahorrar espacio y evitar llevar media cocina de casa. Prioriza piezas apilables y fáciles de limpiar.", "set-cocina"),
        ("11. Cafetera portátil", "Para muchos viajeros, el café de la mañana forma parte del ritual. Una cafetera compacta permite prepararlo sin ocupar demasiado espacio.", "cafetera-portatil"),
        ("12. Botellas reutilizables", "Llevar botellas reutilizables reduce residuos y facilita tener agua a mano durante las rutas y excursiones.", "botellas"),
        ("13. Ducha portátil", "Una ducha portátil puede resultar muy útil después de la playa, una ruta de montaña o una jornada de bicicleta, especialmente cuando el vehículo no dispone de ducha.", "ducha-portatil"),
        ("14. Mesa auxiliar plegable", "Una mesa ligera y plegable amplía el espacio exterior y puede convertirse en zona para comer, cocinar o apoyar el portátil.", "mesa-plegable"),
        ("15. Ganchos para organizar", "Los ganchos adhesivos o soluciones similares permiten aprovechar paredes, puertas y pequeños espacios para colgar toallas, utensilios o accesorios.", "ganchos"),
        ("16. Tendedero portátil", "Un tendedero compacto permite secar bañadores, toallas y ropa después de una jornada de playa o piscina sin ocupar demasiado espacio.", "tendedero"),
        ("17. Detector de humo y monóxido de carbono", "No es el accesorio más divertido de la lista, pero sí uno de los más importantes. Un detector adecuado puede aportar una capa adicional de seguridad en el vehículo. Comprueba siempre que el dispositivo sea apropiado para el uso que vas a darle.", "detector-co"),
        ("18. Kit compacto de herramientas", "Un pequeño juego de herramientas puede resolver ajustes y reparaciones sencillas durante el viaje. Conviene adaptarlo al vehículo y no sustituye una revisión profesional cuando existe una avería importante.", "kit-herramientas"),
        ("19. Linterna LED", "Aunque llevemos el móvil, una linterna independiente sigue siendo muy útil para revisar el exterior, buscar algo por la noche o solucionar una incidencia.", "linterna"),
        ("20. Kit de reparación para camping", "Un pequeño kit con elementos de reparación puede salvar una salida cuando aparece un problema menor. La composición ideal depende del tipo de camper y del equipamiento que lleves.", "kit-reparacion"),
    ]
    body = intro
    body += '<div style="margin:24px 0;padding:18px;border-radius:16px;background:#f5f5f5;"><strong>💡 Consejo:</strong> no necesitas comprar los 20. Elige los que solucionen problemas reales de tu forma de viajar.</div>'
    for heading, text, key in sections:
        item = next(p for p in PRODUCTS if p[0] == key)
        body += f'<h2>{heading}</h2><p>{text}</p><img src="{item[1]}" alt="{item[2]}" loading="lazy" style="width:100%;aspect-ratio:16/9;height:auto;object-fit:cover;border-radius:16px;margin:20px 0;">'
        body += '<p><strong>💶 Precio orientativo:</strong> menos de 50 €.</p><p><strong>👉 Antes de comprar:</strong> comprueba el precio, disponibilidad, medidas y compatibilidad en Amazon.</p>'
    body += """
<h2>¿Realmente necesitas los 20 accesorios?</h2>
<p>No. Esa es precisamente la gracia de esta lista. El mejor equipamiento camper es el que resuelve un problema concreto sin llenar todos los armarios.</p>
<p>Si estás empezando, prioriza iluminación, energía, organización, seguridad y los accesorios relacionados con las actividades que realizas habitualmente. Después puedes ir añadiendo pequeños extras según tus necesidades.</p>
<h2>Conclusión</h2>
<p>Preparar una camper puede convertirse fácilmente en una colección infinita de accesorios. Con un presupuesto moderado, sin embargo, puedes conseguir mejoras muy útiles para viajar con más comodidad y organización.</p>
<p><strong>¿Cuál de estos accesorios llevas siempre en tu camper?</strong> Cuéntanoslo y ampliaremos la lista con nuevas ideas.</p>
"""
    post.content = body
    post.save()


def remove_camper_products(apps, schema_editor):
    Post = apps.get_model("blog", "Post")
    PostImage = apps.get_model("blog", "PostImage")
    post = Post.objects.filter(slug=POST_SLUG).first()
    if post:
        PostImage.objects.filter(post=post).delete()
        post.delete()


class Migration(migrations.Migration):
    dependencies = [("blog", "0013_fix_frescos_verano_images")]
    operations = [migrations.RunPython(add_camper_products, remove_camper_products)]
