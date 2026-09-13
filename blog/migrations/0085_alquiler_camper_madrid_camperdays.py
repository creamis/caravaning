from django.db import migrations
from urllib.parse import quote

POST_SLUG = "alquiler-camper-madrid"
AWIN_MID = "52113"
AWIN_AFFID = "2917197"
CAMPERDAYS_MADRID = "https://www.camperdays.es/autocaravana-espana/madrid.html"


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

    hero_link = awin(CAMPERDAYS_MADRID, "camperdays_post_madrid_inicio")
    prices_link = awin(CAMPERDAYS_MADRID, "camperdays_post_madrid_precios")
    route_link = awin(CAMPERDAYS_MADRID, "camperdays_post_madrid_rutas")
    final_link = awin(CAMPERDAYS_MADRID, "camperdays_post_madrid_final")

    content = f'''
<p>Madrid es mucho más que una gran ciudad para comenzar un viaje. Su posición en el centro de la península la convierte en una base muy práctica para recorrer la Sierra de Guadarrama, Segovia, Ávila, Toledo, Cuenca o incluso plantear una ruta de varios días hacia Castilla y León o Castilla-La Mancha. Si no tienes vehículo propio, alquilar una camper o autocaravana en Madrid puede ser una forma flexible de organizar el viaje a tu ritmo.</p>
<p>En esta guía repasamos cuánto puede costar el alquiler, qué conviene comparar antes de reservar, qué tipo de vehículo elegir y varias rutas interesantes para aprovechar Madrid como punto de salida.</p>
<p><a href="{hero_link}" target="_blank" rel="nofollow sponsored noopener"><strong>🚐 Comparar campers y autocaravanas disponibles en Madrid →</strong></a></p>

<h2>¿Cuánto cuesta alquilar una camper en Madrid?</h2>
<p>El precio depende mucho de las fechas, la duración del viaje, el tamaño del vehículo, el proveedor y la antelación de la reserva. CamperDays muestra actualmente ofertas en Madrid desde alrededor de 61 € por noche, aunque es una referencia cambiante y no un precio garantizado para todas las fechas.</p>
<p>La propia plataforma refleja una diferencia notable entre temporada baja y alta, así que conviene comparar el precio total de la reserva y no quedarse únicamente con la cifra por noche.</p>
<p><a href="{prices_link}" target="_blank" rel="nofollow sponsored noopener"><strong>Consultar precios para mis fechas en CamperDays →</strong></a></p>

<h2>Qué debes comparar además del precio</h2>
<ul>
<li><strong>Kilómetros incluidos:</strong> si vas a hacer una ruta larga, comprueba si son ilimitados o existe un máximo diario.</li>
<li><strong>Franquicia y depósito:</strong> revisa cuánto tendrás que dejar como garantía y las condiciones del seguro.</li>
<li><strong>Punto de recogida:</strong> algunas bases están en Madrid capital y otras en localidades cercanas como Alcalá de Henares.</li>
<li><strong>Equipamiento:</strong> cocina, baño, ducha, climatización, ropa de cama y mobiliario exterior varían según el vehículo.</li>
<li><strong>Cancelación:</strong> revisa las condiciones si reservas con bastante antelación.</li>
<li><strong>Mascotas:</strong> hay vehículos que las admiten, pero no todos. Filtra la búsqueda si viajas con perro.</li>
</ul>

<h2>Camper compacta o autocaravana grande</h2>
<p>Para una pareja que piensa hacer muchos kilómetros, entrar en pueblos y moverse con frecuencia, una camper compacta suele ser más sencilla de conducir y estacionar. Para familias o viajes de una semana o más, una autocaravana con baño completo, más camas y mayor espacio interior puede resultar mucho más cómoda.</p>
<p>Antes de reservar piensa cuántas personas van a dormir, cuánto equipaje lleváis, si necesitáis ducha y WC y cuánto tiempo vais a pasar dentro del vehículo.</p>

<h2>Ruta 1: Madrid y Sierra de Guadarrama</h2>
<p>Una de las escapadas más fáciles desde Madrid es dirigirse hacia la Sierra de Guadarrama. Puedes combinar lugares como Navacerrada, Cercedilla, Rascafría o el entorno de El Escorial con rutas de senderismo y noches en campings o áreas autorizadas.</p>
<p>Es una buena opción para un fin de semana o para comenzar una ruta más larga hacia Segovia.</p>

<h2>Ruta 2: Madrid, Segovia y Ávila</h2>
<p>Con varios días disponibles puedes salir de Madrid hacia Segovia, continuar hasta Ávila y regresar después por la sierra. Es una ruta muy completa si buscas patrimonio, gastronomía y carreteras interiores sin hacer distancias enormes cada día.</p>
<p>Planifica previamente las zonas de pernocta y evita improvisar en cascos históricos o lugares con restricciones específicas para autocaravanas.</p>

<h2>Ruta 3: Madrid y Toledo</h2>
<p>Otra alternativa sencilla consiste en dirigirte hacia Toledo y continuar después hacia localidades de Castilla-La Mancha. Es una ruta especialmente cómoda si tienes pocos días y quieres combinar ciudad histórica con carreteras tranquilas y paisajes de interior.</p>
<p><a href="{route_link}" target="_blank" rel="nofollow sponsored noopener"><strong>Ver vehículos disponibles para empezar tu ruta desde Madrid →</strong></a></p>

<h2>Ruta 4: una semana por el centro de España</h2>
<p>Con siete días puedes plantear una ruta circular desde Madrid pasando por Segovia, Ávila, Toledo y algún tramo de la Sierra de Guadarrama. La ventaja de salir desde el centro de España es que puedes modificar el itinerario con facilidad según el tiempo, el tráfico o las ganas de conducir.</p>
<p>No intentes llenar cada jornada con demasiados kilómetros. Viajar en camper funciona mejor cuando dejas margen para parar, caminar y disfrutar de los lugares que vas encontrando.</p>

<h2>¿Dónde se recogen las campers de alquiler?</h2>
<p>La disponibilidad cambia según las fechas y el proveedor. Actualmente CamperDays muestra puntos de recogida en Madrid y alrededores, incluyendo Madrid capital y Alcalá de Henares. Comprueba siempre la dirección exacta antes de reservar y calcula cómo llegar desde el aeropuerto, la estación de tren o tu alojamiento.</p>

<h2>Documentación, edad y depósito</h2>
<p>Antes de pagar revisa las condiciones del proveedor elegido. Normalmente necesitarás documentación de identidad, un permiso de conducir válido y una tarjeta aceptada para el depósito. La edad mínima del conductor y la antigüedad exigida del permiso pueden variar según la compañía y el vehículo.</p>

<h2>¿Dónde dormir con la camper?</h2>
<p>No debes confundir estacionar con acampar. Sacar toldo, mesas, sillas u otros elementos al exterior puede convertir una simple parada en acampada. Además, existen restricciones municipales y normas específicas en determinados espacios naturales.</p>
<p>Para una ruta tranquila, combina áreas de autocaravanas y campings y comprueba siempre la señalización del lugar en el que piensas pasar la noche.</p>

<h2>Consejos para ahorrar en el alquiler</h2>
<ul>
<li>Compara varias fechas si tienes flexibilidad.</li>
<li>Evita concentrar la búsqueda únicamente en agosto, Semana Santa y puentes.</li>
<li>Reserva con antelación si necesitas un vehículo familiar concreto.</li>
<li>Compara el precio total con seguro, extras y kilometraje incluidos.</li>
<li>No alquiles una autocaravana más grande de lo que realmente necesitas.</li>
</ul>

<h2>Prepara el viaje antes de recoger el vehículo</h2>
<p>Cuando tengas la reserva, prepara una lista sencilla con documentación, ropa, cocina, agua, carga de dispositivos y accesorios para dormir. Puedes consultar nuestra <a href="/blog/escapada-fin-de-semana-autocaravana/"><strong>guía para una escapada de fin de semana en autocaravana</strong></a> y nuestra selección de <a href="/shop/"><strong>accesorios para camper y camping</strong></a>.</p>
<p>Si vas a utilizar campings durante la ruta, también puedes explorar nuestra sección de <a href="/camping/"><strong>campings</strong></a>.</p>

<h2>Comparar alquiler de camper en Madrid</h2>
<p>Cuando tengas claras las fechas, el número de viajeros y el tipo de vehículo, compara varias opciones antes de reservar. Fíjate especialmente en el precio total, la franquicia, el depósito, los kilómetros incluidos y el punto de recogida.</p>
<p><a href="{final_link}" target="_blank" rel="nofollow sponsored noopener"><strong>🚐 Buscar camper o autocaravana en Madrid con CamperDays →</strong></a></p>
<hr>
<p><small>Este artículo contiene enlaces de afiliado. Si realizas una reserva a través de ellos, Caravaning Project puede recibir una comisión sin coste adicional para ti. Precios, disponibilidad y condiciones pueden cambiar; comprueba siempre la información final antes de reservar.</small></p>
'''

    Post.objects.create(
        slug=POST_SLUG,
        title="Alquiler de camper en Madrid: precios, rutas y consejos para viajar",
        content=content,
        meta_description="Guía para alquilar camper o autocaravana en Madrid: precios orientativos, rutas, puntos de recogida y consejos antes de reservar.",
        status="PUBLISHED",
        author=author,
    )


class Migration(migrations.Migration):
    dependencies = [
        ("blog", "0084_restaurar_imagenes_generadas_valencia_media"),
    ]

    operations = [
        migrations.RunPython(create_post, migrations.RunPython.noop),
    ]
