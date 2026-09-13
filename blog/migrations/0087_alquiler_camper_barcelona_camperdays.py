from django.db import migrations
from urllib.parse import quote

POST_SLUG = "alquiler-camper-barcelona"
AWIN_MID = "52113"
AWIN_AFFID = "2917197"
CAMPERDAYS_BARCELONA = "https://www.camperdays.es/autocaravana-espana/barcelona.html"


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

    hero_link = awin(CAMPERDAYS_BARCELONA, "camperdays_post_barcelona_inicio")
    prices_link = awin(CAMPERDAYS_BARCELONA, "camperdays_post_barcelona_precios")
    routes_link = awin(CAMPERDAYS_BARCELONA, "camperdays_post_barcelona_rutas")
    final_link = awin(CAMPERDAYS_BARCELONA, "camperdays_post_barcelona_final")

    content = f'''
<p>Barcelona es uno de los mejores puntos de salida para una ruta en camper por el noreste de España. Desde la ciudad puedes enlazar en pocas horas con la Costa Brava, el Montseny, los Pirineos, Tarragona o incluso preparar una ruta circular por Cataluña y Aragón.</p>
<p>Si no tienes vehículo propio, alquilar una camper o autocaravana en Barcelona te permite adaptar el viaje a tus días disponibles, al número de viajeros y al tipo de ruta que quieras hacer.</p>
<p><a href="{hero_link}" target="_blank" rel="nofollow sponsored noopener"><strong>🚐 Comparar campers y autocaravanas disponibles en Barcelona →</strong></a></p>

<h2>¿Cuánto cuesta alquilar una camper en Barcelona?</h2>
<p>El precio depende de las fechas, la duración del alquiler, el tamaño del vehículo y el proveedor. Como referencia orientativa, CamperDays muestra actualmente opciones en Barcelona desde unos 62 € por noche, aunque el importe real puede cambiar según disponibilidad y temporada.</p>
<p>Además del precio por noche, conviene revisar el coste total de la reserva, los kilómetros incluidos, la franquicia, el depósito y los posibles extras.</p>
<p><a href="{prices_link}" target="_blank" rel="nofollow sponsored noopener"><strong>Consultar precios para mis fechas en CamperDays →</strong></a></p>

<h2>Qué comparar antes de reservar</h2>
<ul>
<li><strong>Kilometraje:</strong> algunas ofertas incluyen kilómetros ilimitados y otras establecen límites.</li>
<li><strong>Seguro y franquicia:</strong> revisa qué cubre la tarifa y cuánto asumirías en caso de incidencia.</li>
<li><strong>Depósito:</strong> comprueba el importe y el método de pago exigido por la empresa de alquiler.</li>
<li><strong>Punto de recogida:</strong> muchas bases están en municipios próximos a Barcelona, así que calcula también el desplazamiento.</li>
<li><strong>Equipamiento:</strong> cocina, baño, ducha, aire acondicionado, calefacción, ropa de cama o mobiliario exterior pueden variar.</li>
<li><strong>Mascotas:</strong> si viajas con perro, filtra solo los vehículos que las admitan.</li>
</ul>

<h2>Camper compacta o autocaravana grande</h2>
<p>Para una pareja que quiere recorrer la Costa Brava, visitar pueblos y cambiar de lugar casi a diario, una camper compacta puede ser muy práctica. Si viajas en familia o piensas pasar más tiempo dentro del vehículo, una autocaravana con baño, ducha y mayor capacidad de almacenamiento suele resultar más cómoda.</p>
<p>Antes de reservar piensa en cuántas personas van a dormir, el volumen de equipaje, si necesitas baño completo y cuánto tiempo pasarás conduciendo frente al tiempo que estarás instalado en áreas o campings.</p>

<h2>Ruta 1: Barcelona y Costa Brava</h2>
<p>Una de las rutas más atractivas desde Barcelona es subir hacia la Costa Brava. Puedes enlazar lugares como Tossa de Mar, Sant Feliu de Guíxols, Begur, Pals o Cadaqués, combinando calas, pueblos históricos y carreteras panorámicas.</p>
<p>En temporada alta conviene reservar con antelación tanto el vehículo como los campings o áreas que tengas claro que vas a utilizar.</p>

<h2>Ruta 2: Barcelona, Montseny y Pirineos</h2>
<p>Si prefieres montaña, desde Barcelona puedes dirigirte hacia el Parque Natural del Montseny y continuar hacia zonas prepirenaicas o pirenaicas. Es una opción muy interesante en primavera y otoño, cuando las temperaturas son más suaves y muchas rutas de senderismo resultan especialmente agradables.</p>
<p><a href="{routes_link}" target="_blank" rel="nofollow sponsored noopener"><strong>Ver vehículos disponibles para empezar una ruta desde Barcelona →</strong></a></p>

<h2>Ruta 3: Barcelona, Tarragona y el interior</h2>
<p>Otra posibilidad es bajar hacia Sitges y Tarragona para después entrar hacia el interior. Con una semana disponible puedes plantear una ruta circular que combine costa, patrimonio y naturaleza sin acumular demasiadas horas de conducción cada día.</p>
<p>CamperDays también propone Barcelona como punto de partida para itinerarios que conectan Tarragona, Zaragoza, Pamplona, San Sebastián, Aínsa y Lleida antes de regresar a Barcelona.</p>

<h2>¿Dónde se recogen las campers de alquiler?</h2>
<p>La disponibilidad cambia según las fechas y el proveedor. En las búsquedas actuales de CamperDays aparecen opciones en Barcelona y municipios próximos como Viladecans. Comprueba siempre la dirección exacta de la estación antes de confirmar la reserva.</p>
<p>Si llegas en avión o tren, calcula el coste y el tiempo del traslado hasta la base de recogida antes de comparar dos ofertas aparentemente similares.</p>

<h2>Mejor época para viajar en camper desde Barcelona</h2>
<p>Primavera y otoño suelen ofrecer un buen equilibrio entre temperaturas suaves, menos saturación turística y mejores condiciones para combinar ciudad, playa y montaña. En verano aumenta la demanda, especialmente en la costa, por lo que reservar con antelación cobra todavía más importancia.</p>

<h2>Documentación y depósito</h2>
<p>Revisa siempre las condiciones del proveedor. Normalmente necesitarás documento de identidad, permiso de conducir válido y una tarjeta aceptada para bloquear el depósito. La edad mínima del conductor y la antigüedad del permiso pueden variar entre empresas.</p>

<h2>¿Se puede dormir en cualquier lugar?</h2>
<p>No debes confundir estacionar con acampar. Sacar toldo, mesas, sillas o elementos fuera del vehículo puede cambiar la consideración de la parada. Además, los municipios y espacios naturales pueden aplicar restricciones específicas. Comprueba siempre la señalización local y utiliza áreas o campings cuando corresponda.</p>

<h2>Consejos para reducir el coste del alquiler</h2>
<ul>
<li>Compara varias fechas si tienes flexibilidad.</li>
<li>Evita concentrar la búsqueda únicamente en agosto y puentes.</li>
<li>Reserva con antelación en temporada alta.</li>
<li>Compara el precio total y no solo el importe diario.</li>
<li>Elige el tamaño de camper que realmente necesitas.</li>
<li>Revisa si los kilómetros están incluidos o son ilimitados.</li>
</ul>

<h2>Prepara la ruta antes de recoger el vehículo</h2>
<p>Antes de salir prepara documentación, ropa, carga de dispositivos, agua, cocina y equipamiento para dormir. Si vas a hacer una escapada corta, puedes consultar nuestra <a href="/blog/escapada-fin-de-semana-autocaravana/"><strong>guía para una escapada de fin de semana en autocaravana</strong></a>.</p>
<p>También puedes revisar nuestra <a href="/shop/"><strong>selección de accesorios para camper y camping</strong></a> y la sección de <a href="/camping/"><strong>campings</strong></a> para organizar algunas noches de la ruta.</p>

<h2>Comparar alquiler de camper en Barcelona</h2>
<p>Cuando tengas claras las fechas, el número de viajeros y el tipo de vehículo, compara varias opciones fijándote en precio total, depósito, franquicia, kilometraje y punto de recogida.</p>
<p><a href="{final_link}" target="_blank" rel="nofollow sponsored noopener"><strong>🚐 Buscar camper o autocaravana en Barcelona con CamperDays →</strong></a></p>
<hr>
<p><small>Este artículo contiene enlaces de afiliado. Si realizas una reserva a través de ellos, Caravaning Project puede recibir una comisión sin coste adicional para ti. Precios, disponibilidad y condiciones pueden cambiar; comprueba siempre la información final antes de reservar.</small></p>
'''

    Post.objects.create(
        slug=POST_SLUG,
        title="Alquiler de camper en Barcelona: precios, rutas y consejos para viajar",
        content=content,
        meta_description="Guía para alquilar camper o autocaravana en Barcelona: precios orientativos, Costa Brava, Pirineos, rutas y consejos antes de reservar.",
        status="PUBLISHED",
        author=author,
    )


class Migration(migrations.Migration):
    dependencies = [
        ("blog", "0086_imagenes_generadas_alquiler_camper_madrid"),
    ]

    operations = [
        migrations.RunPython(create_post, migrations.RunPython.noop),
    ]
