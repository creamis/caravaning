from django.db import migrations
from urllib.parse import quote

POST_SLUG = "campings-montana-naturaleza-espana"
AWIN_MID = "13054"
AWIN_AFFID = "2917197"


def awin(destination):
    return (
        "https://www.awin1.com/cread.php?"
        f"awinmid={AWIN_MID}&awinaffid={AWIN_AFFID}&ued={quote(destination, safe='')}"
    )


CAMPINGS = [
    (
        "Wecamp Pirineos",
        "Boltaña, Huesca",
        "En pleno Sobrarbe y a los pies de los Pirineos aragoneses. Es una base muy interesante para combinar rutas, pueblos de montaña y naturaleza.",
        "https://es.camping-and-co.com/camping-pirineos",
    ),
    (
        "Peña Montañesa",
        "Labuerda, Huesca",
        "Una opción especialmente atractiva para explorar el entorno de Aínsa, el río Cinca y los paisajes del Pirineo aragonés, con Ordesa y Monte Perdido como gran referencia de la zona.",
        "https://es.camping-and-co.com/camping-pena-montanesa",
    ),
    (
        "Barcelona Pirineos",
        "Sant Julià de Cerdanyola, Barcelona",
        "Una propuesta claramente montañera para quienes buscan aire puro, tranquilidad y actividades al aire libre en el entorno prepirenaico catalán.",
        "https://es.camping-and-co.com/camping-barcelona-pirineos",
    ),
    (
        "Camping Pirinenc",
        "Campdevànol, Girona",
        "Rodeado de montañas y grandes espacios, encaja bien en una ruta por el Pirineo catalán y para escapadas centradas en senderismo y pueblos de montaña.",
        "https://es.camping-and-co.com/camping-pirinenc",
    ),
    (
        "Camping Urbión",
        "Abejar, Soria",
        "Bosques de pinos, relieves montañosos y la cercanía del embalse de la Cuerda del Pozo lo convierten en una alternativa distinta para desconectar en plena naturaleza.",
        "https://es.camping-and-co.com/camping-urbion",
    ),
    (
        "Camping Sierra Calderona",
        "Estivella, Valencia",
        "Situado entre montañas y próximo al Parque Natural de la Sierra Calderona. Es una buena base para senderismo, bicicleta de montaña y escapadas de naturaleza sin alejarse demasiado de la costa valenciana.",
        "https://es.camping-and-co.com/camping-sierra-calderona",
    ),
    (
        "Camping El Llosar",
        "Villafranca del Cid, Castellón",
        "En las montañas de Els Ports, ofrece un ambiente tranquilo y un entorno apropiado para quienes prefieren naturaleza, pueblos del interior y ritmos de viaje más pausados.",
        "https://es.camping-and-co.com/camping-llosar",
    ),
]


def create_post(apps, schema_editor):
    Post = apps.get_model("blog", "Post")
    User = apps.get_model("auth", "User")

    if Post.objects.filter(slug=POST_SLUG).exists():
        return

    author = User.objects.filter(is_superuser=True).order_by("id").first() or User.objects.order_by("id").first()
    if not author:
        return

    sections = []
    for index, (name, location, description, destination) in enumerate(CAMPINGS, start=1):
        sections.append(f'''<h2>{index}. {name} · {location}</h2>
<p>{description}</p>
<p><a href="{awin(destination)}" target="_blank" rel="nofollow sponsored noopener"><strong>Consultar precios y disponibilidad en Camping &amp; Co →</strong></a></p>''')

    content = f'''
<p>España tiene muchas rutas de interior en las que la propia estancia forma parte del viaje. Pirineos, bosques, embalses y sierras permiten cambiar la playa por senderos, aire fresco y noches rodeadas de naturaleza.</p>
<p>Hemos seleccionado siete campings de montaña y naturaleza que no aparecen en nuestras anteriores selecciones de campings de playa o familiares. Antes de reservar, comprueba siempre qué tipo de parcela admite tu camper, caravana o autocaravana y las fechas de apertura del establecimiento.</p>
{''.join(sections)}
<h2>Qué llevar a un camping de montaña</h2>
<p>En zonas de montaña el tiempo puede cambiar con rapidez. Una prenda impermeable, calzado adecuado, iluminación portátil y algo de abrigo adicional suelen ser más útiles que llenar el vehículo de accesorios poco utilizados.</p>
<p><a href="/shop/"><strong>Ver nuestra selección de equipamiento camper y camping →</strong></a></p>
<p>Si viajas cuando bajan las temperaturas, también puedes consultar nuestra guía sobre <a href="/blog/viajar-camper-invierno/"><strong>qué necesitas para viajar con una camper en invierno</strong></a>.</p>
<h2>Antes de reservar</h2>
<p>Comprueba accesos, dimensiones de parcela, electricidad, servicios disponibles y política de mascotas si viajas con animales. En zonas de montaña también conviene revisar la previsión meteorológica y el estado de las carreteras antes de iniciar la ruta.</p>
<hr>
<p><small>Este artículo contiene enlaces de afiliado. Si realizas una reserva a través de ellos, Caravaning Project puede recibir una comisión sin coste adicional para ti.</small></p>
'''

    Post.objects.create(
        slug=POST_SLUG,
        title="7 campings de montaña y naturaleza en España para camper, caravana o autocaravana",
        content=content,
        meta_description="Descubre 7 campings de montaña y naturaleza en España para viajar en camper, caravana o autocaravana: Pirineos, Soria, Valencia y Castellón.",
        status="PUBLISHED",
        author=author,
    )


class Migration(migrations.Migration):
    dependencies = [
        ("blog", "0073_imagenes_campings_ninos_espana"),
    ]

    operations = [
        migrations.RunPython(create_post, migrations.RunPython.noop),
    ]
