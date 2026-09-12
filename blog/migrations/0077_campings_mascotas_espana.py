from django.db import migrations
from urllib.parse import quote

POST_SLUG = "campings-admiten-mascotas-espana"
AWIN_MID = "13054"
AWIN_AFFID = "2917197"


def awin(destination):
    return (
        "https://www.awin1.com/cread.php?"
        f"awinmid={AWIN_MID}&awinaffid={AWIN_AFFID}&ued={quote(destination, safe='')}"
    )


CAMPINGS = [
    (
        "Camping Lo Monte",
        "Pilar de la Horadada, Alicante",
        "Camping & Co muestra opciones de alojamiento que admiten mascotas. Además, está cerca de la costa y puede encajar bien en una escapada por el sur de Alicante.",
        "https://es.camping-and-co.com/camping-lo-monte",
    ),
    (
        "Camping L'Alqueria",
        "Gandia, Valencia",
        "Una alternativa en la costa valenciana donde Camping & Co indica disponibilidad de alojamientos que admiten animales. Conviene confirmar siempre las condiciones concretas al reservar.",
        "https://es.camping-and-co.com/camping-alqueria",
    ),
    (
        "Camping Castello Mar",
        "Castelló d'Empúries, Girona",
        "Una opción de la Costa Brava próxima a Empuriabrava. Camping & Co muestra alojamientos que permiten mascotas, por lo que puede resultar interesante para combinar playa y paseos con tu perro.",
        "https://es.camping-and-co.com/camping-castello-mar",
    ),
    (
        "Camping Cabopino",
        "Marbella, Málaga",
        "Situado en la Costa del Sol y cerca de la playa. Algunas de las opciones publicadas por Camping & Co admiten mascotas, así que es importante seleccionar expresamente una de ellas antes de completar la reserva.",
        "https://es.camping-and-co.com/camping-cabopino",
    ),
    (
        "Wecamp Santa Cristina",
        "Santa Cristina d'Aro, Girona",
        "Una base interesante para descubrir el interior de la Costa Brava. Camping & Co muestra varias opciones pet friendly, aunque la aceptación depende del alojamiento elegido.",
        "https://es.camping-and-co.com/camping-santa-cristina",
    ),
    (
        "Camping Taïga Conil",
        "Conil de la Frontera, Cádiz",
        "Una propuesta del litoral gaditano donde Camping & Co indica alojamientos que admiten mascotas. Buena opción para combinar camping, costa y rutas por los alrededores de Conil.",
        "https://es.camping-and-co.com/camping-conil",
    ),
    (
        "Camping Sol de Calpe Boreal",
        "Calpe, Alicante",
        "Una alternativa para viajar con mascota por la Costa Blanca. Camping & Co muestra alojamientos que admiten animales y el camping se encuentra relativamente cerca de las playas de Calpe.",
        "https://es.camping-and-co.com/camping-sol-de-calpe-boreal",
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
<p><a href="{awin(destination)}" target="_blank" rel="nofollow sponsored noopener"><strong>Consultar alojamientos y disponibilidad en Camping &amp; Co →</strong></a></p>''')

    content = f'''
<p>Viajar en camper, caravana o autocaravana con perro es cada vez más habitual, pero no todos los campings aplican la misma política de admisión. Algunos permiten mascotas únicamente en determinados alojamientos, parcelas o temporadas.</p>
<p>Por eso hemos seleccionado siete campings de España en los que Camping &amp; Co muestra opciones que admiten animales. Antes de reservar, comprueba siempre las condiciones concretas del alojamiento elegido, posibles suplementos, límites de tamaño o número de mascotas y las normas de las zonas comunes.</p>
{''.join(sections)}
<h2>Qué revisar antes de viajar con tu perro</h2>
<ul>
<li>Que la parcela o alojamiento seleccionado admita mascotas de forma expresa.</li>
<li>Posibles suplementos por noche o por estancia.</li>
<li>Normas sobre correa, zonas comunes y acceso a piscinas o restaurantes.</li>
<li>Documentación, identificación y cartilla sanitaria del animal.</li>
<li>Zonas de paseo cercanas y restricciones en playas durante la temporada alta.</li>
</ul>
<h2>Qué llevar en la camper o autocaravana</h2>
<p>Agua y bebedero, correa o arnés, bolsas, una manta o cama conocida, comida suficiente y una pequeña toalla suelen cubrir lo esencial. En verano es especialmente importante evitar que el animal permanezca solo dentro del vehículo cuando la temperatura pueda subir.</p>
<p><a href="/shop/"><strong>Ver nuestra selección de accesorios para camper y camping →</strong></a></p>
<p>Si estás preparando una salida corta, también puedes consultar nuestra guía <a href="/blog/escapada-fin-de-semana-autocaravana/"><strong>qué llevar para una escapada de fin de semana en autocaravana</strong></a>.</p>
<h2>Importante: comprueba la política antes de reservar</h2>
<p>La admisión de mascotas puede variar según fechas, tipo de alojamiento y condiciones del propio camping. Usa los enlaces anteriores para consultar la disponibilidad actual y revisa la política específica de la opción que vayas a reservar.</p>
<hr>
<p><small>Este artículo contiene enlaces de afiliado. Si realizas una reserva a través de ellos, Caravaning Project puede recibir una comisión sin coste adicional para ti.</small></p>
'''

    Post.objects.create(
        slug=POST_SLUG,
        title="7 campings que admiten mascotas en España para viajar con perro",
        content=content,
        meta_description="Descubre 7 campings en España con opciones que admiten mascotas para viajar con perro en camper, caravana o autocaravana.",
        status="PUBLISHED",
        author=author,
    )


class Migration(migrations.Migration):
    dependencies = [
        ("blog", "0076_corregir_imagenes_campings_montana"),
    ]

    operations = [
        migrations.RunPython(create_post, migrations.RunPython.noop),
    ]
