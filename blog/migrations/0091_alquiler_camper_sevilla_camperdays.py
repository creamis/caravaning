from django.db import migrations
from urllib.parse import quote

POST_SLUG = "alquiler-camper-sevilla"
AWIN_MID = "52113"
AWIN_AFFID = "2917197"
CAMPERDAYS_SEVILLA = "https://www.camperdays.es/autocaravana-espana/sevilla.html"


def awin(destination, clickref):
    return (
        "https://www.awin1.com/cread.php?"
        f"awinmid={AWIN_MID}&awinaffid={AWIN_AFFID}"
        f"&clickref={clickref}&ued={quote(destination, safe='')}"
    )


def create_post(apps, schema_editor):
    Post = apps.get_model("blog", "Post")
    User = apps.get_model("auth", "User")

    if Post.objects.filter(slug=POST_SLUG).exists():
        return

    author = User.objects.filter(is_superuser=True).order_by("id").first() or User.objects.order_by("id").first()
    if not author:
        return

    hero = awin(CAMPERDAYS_SEVILLA, "camperdays_post_sevilla_inicio")
    prices = awin(CAMPERDAYS_SEVILLA, "camperdays_post_sevilla_precios")
    routes = awin(CAMPERDAYS_SEVILLA, "camperdays_post_sevilla_rutas")
    final = awin(CAMPERDAYS_SEVILLA, "camperdays_post_sevilla_final")

    content = f'''
<p>Sevilla es un excelente punto de partida para descubrir Andalucía en camper o autocaravana. Desde la capital puedes combinar ciudades monumentales, pueblos históricos, naturaleza y costa sin depender de un itinerario cerrado.</p>
<p>Si no tienes vehículo propio, CamperDays permite comparar diferentes campers y autocaravanas disponibles en Sevilla y sus alrededores, con opciones de distintos proveedores y capacidades.</p>
<p><a href="{hero}" target="_blank" rel="nofollow sponsored noopener noreferrer"><strong>🚐 Comparar campers y autocaravanas disponibles en Sevilla →</strong></a></p>

<h2>¿Cuánto cuesta alquilar una camper en Sevilla?</h2>
<p>El precio cambia según las fechas, duración del viaje, tipo de vehículo, proveedor y equipamiento. En CamperDays pueden encontrarse ofertas desde aproximadamente 64 € por noche en determinadas fechas, aunque es solo una referencia y el precio real de tu viaje puede ser diferente.</p>
<p>Para comparar bien no mires únicamente el precio por noche. Revisa también el coste total de la reserva, kilometraje, seguro, franquicia, depósito y posibles extras.</p>
<p><a href="{prices}" target="_blank" rel="nofollow sponsored noopener noreferrer"><strong>Consultar precios y disponibilidad en Sevilla →</strong></a></p>

<h2>¿Dónde se recogen las campers en Sevilla?</h2>
<p>Los puntos de recogida dependen del proveedor y del vehículo elegido. CamperDays muestra opciones en Sevilla y alrededores, incluyendo proveedores con recogida en Sevilla y Dos Hermanas.</p>
<p>Comprueba siempre la dirección exacta, horario de recogida y condiciones antes de reservar, especialmente si llegas a Sevilla en avión o tren.</p>

<h2>Qué comparar antes de reservar</h2>
<ul>
<li><strong>Kilometraje:</strong> comprueba si es ilimitado o existe un máximo incluido.</li>
<li><strong>Seguro y franquicia:</strong> revisa qué cubre la tarifa y qué cantidad asumirías en caso de daños.</li>
<li><strong>Depósito:</strong> consulta el importe y el tipo de tarjeta exigido por el proveedor.</li>
<li><strong>Equipamiento:</strong> cocina, ducha, WC, aire acondicionado, ropa de cama y mobiliario pueden variar.</li>
<li><strong>Capacidad:</strong> una camper para dos personas puede ser más manejable que una autocaravana familiar.</li>
<li><strong>Recogida y devolución:</strong> confirma horarios y ubicación antes de organizar el resto del viaje.</li>
</ul>

<h2>Camper pequeña o autocaravana</h2>
<p>Para una pareja que quiera moverse con frecuencia por pueblos y ciudades, una camper compacta puede resultar especialmente cómoda. Para familias o viajes largos, una autocaravana con baño completo, más camas y almacenamiento puede compensar el mayor tamaño.</p>

<h2>Ruta 1: Sevilla, Carmona, Écija y Osuna</h2>
<p>Una ruta muy completa desde Sevilla permite enlazar Carmona, Écija y Osuna. Es una combinación ideal de patrimonio, gastronomía y pueblos históricos, y puede hacerse con calma dedicando varios días al recorrido.</p>

<h2>Ruta 2: Sierra Norte de Sevilla</h2>
<p>Si prefieres naturaleza, puedes dirigirte hacia la Sierra Norte y recorrer localidades como Constantina, Cazalla de la Sierra, San Nicolás del Puerto o Alanís. Es una alternativa especialmente interesante fuera de los meses de mayor calor.</p>

<h2>Ruta 3: Sevilla hacia Cádiz y la costa</h2>
<p>Con varios días disponibles puedes salir de Sevilla hacia el sur y continuar hasta Cádiz y la costa atlántica. Jerez de la Frontera, El Puerto de Santa María y otros puntos de la provincia permiten construir una ruta muy diferente a la del interior.</p>
<p><a href="{routes}" target="_blank" rel="nofollow sponsored noopener noreferrer"><strong>Ver campers disponibles para empezar una ruta desde Sevilla →</strong></a></p>

<h2>¿Cuál es la mejor época para viajar?</h2>
<p>Primavera y otoño suelen ser épocas especialmente atractivas para recorrer Sevilla y su provincia en camper. Durante el verano las temperaturas pueden ser muy altas, por lo que conviene planificar desplazamientos, zonas de sombra y lugares de pernocta con especial cuidado.</p>
<p>Semana Santa y la Feria de Abril generan una demanda turística muy elevada. Si quieres viajar alrededor de esas fechas, reservar el vehículo y los alojamientos o campings con antelación puede ser importante.</p>

<h2>Documentación y tarjeta de crédito</h2>
<p>Las condiciones concretas dependen del proveedor. Habitualmente necesitarás documentación de identidad, permiso de conducir válido y una tarjeta de crédito vigente para el depósito. Comprueba también la edad mínima y la antigüedad del permiso exigidas para el vehículo elegido.</p>

<h2>Pernoctar con camper en Sevilla</h2>
<p>Recuerda distinguir entre estacionar y acampar. Desplegar toldos, sacar mesas o sillas y ocupar espacio exterior puede estar sujeto a normas diferentes. Respeta siempre la señalización y las restricciones municipales, y utiliza campings o áreas autorizadas cuando corresponda.</p>

<h2>Consejos para ahorrar en el alquiler</h2>
<ul>
<li>Compara varias fechas si tienes flexibilidad.</li>
<li>Reserva con antelación para primavera, festivos y temporada alta.</li>
<li>Elige el tamaño de vehículo que realmente necesitas.</li>
<li>Compara el precio final incluyendo seguro, kilometraje y extras.</li>
<li>Revisa el punto de recogida antes de elegir únicamente por precio.</li>
</ul>

<h2>Prepara tu viaje desde Sevilla</h2>
<p>Antes de recoger el vehículo puedes consultar nuestra <a href="/blog/escapada-fin-de-semana-autocaravana/"><strong>guía para una escapada en autocaravana</strong></a>, revisar nuestros <a href="/shop/"><strong>accesorios para camper y camping</strong></a> y explorar la sección de <a href="/camping/"><strong>campings</strong></a>.</p>

<h2>Comparar alquiler de camper en Sevilla</h2>
<p>Cuando tengas las fechas y el número de viajeros, compara varias opciones y presta atención al coste total, franquicia, depósito, kilometraje, equipamiento y punto real de recogida.</p>
<p><a href="{final}" target="_blank" rel="nofollow sponsored noopener noreferrer"><strong>🚐 Buscar camper o autocaravana en Sevilla con CamperDays →</strong></a></p>
<hr>
<p><small>Este artículo contiene enlaces de afiliado. Si realizas una reserva a través de ellos, Caravaning Project puede recibir una comisión sin coste adicional para ti. Precios, disponibilidad y condiciones pueden cambiar; comprueba siempre la información final antes de reservar.</small></p>
'''

    Post.objects.create(
        slug=POST_SLUG,
        title="Alquiler de camper en Sevilla: precios, rutas y consejos para tu viaje",
        content=content,
        meta_description="Guía para alquilar camper o autocaravana en Sevilla: precios orientativos, puntos de recogida, rutas por Andalucía y consejos antes de reservar.",
        status="PUBLISHED",
        author=author,
    )


class Migration(migrations.Migration):
    dependencies = [
        ("blog", "0090_imagenes_generadas_alquiler_camper_malaga"),
    ]

    operations = [
        migrations.RunPython(create_post, migrations.RunPython.noop),
    ]
