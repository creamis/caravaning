from django.db import migrations
from urllib.parse import quote


POST_SLUG = "campings-para-ir-con-ninos-espana"
AWIN_MID = "13054"
AWIN_AFFID = "2917197"


def awin(destination):
    return (
        "https://www.awin1.com/cread.php?"
        f"awinmid={AWIN_MID}&awinaffid={AWIN_AFFID}&ued={quote(destination, safe='')}"
    )


CAMPINGS = [
    (
        "Camping Creixell Camping & Family Resort",
        "Costa Dorada, Tarragona",
        "Una opción muy enfocada a familias: piscina, tobogán acuático, animación y club infantil, además de playa a unos 150 metros.",
        "https://es.camping-and-co.com/camping-creixell-camping-and-family-resort",
    ),
    (
        "Camping Vilanova Park",
        "Vilanova i la Geltrú, Barcelona",
        "Combina piscina, animación y club infantil. Es una alternativa interesante para familias que buscan actividades dentro del camping y excursiones por la costa catalana.",
        "https://es.camping-and-co.com/camping-vilanova-park",
    ),
    (
        "Camping La Torre del Sol",
        "Costa Dorada, Tarragona",
        "Destaca por su club infantil, animación y cercanía al mar, una combinación muy cómoda cuando se viaja con niños.",
        "https://es.camping-and-co.com/camping-la-torre-del-sol",
    ),
    (
        "Camping Roca Grossa",
        "Calella, Barcelona",
        "Una alternativa familiar con piscina y club infantil, adecuada para combinar días de camping con playa y visitas por la costa de Barcelona.",
        "https://es.camping-and-co.com/camping-roca-grossa",
    ),
    (
        "Camping Prades Park",
        "Prades, Tarragona",
        "Una opción para cambiar la playa por naturaleza y montaña. Cuenta con piscina y animación, por lo que puede funcionar muy bien para unas vacaciones familiares más activas.",
        "https://es.camping-and-co.com/camping-prades-park",
    ),
    (
        "Camping Alannia Guardamar",
        "Guardamar del Segura, Alicante",
        "Piscina y animación en un destino mediterráneo muy familiar. Es una opción especialmente atractiva para quienes buscan combinar camping, playa y actividades para los pequeños.",
        "https://es.camping-and-co.com/camping-alannia-guardamar",
    ),
    (
        "Camping Resort Almafra",
        "Benidorm, Alicante",
        "Dispone de club infantil y animación y permite combinar los servicios del camping con excursiones y planes familiares por la Costa Blanca.",
        "https://es.camping-and-co.com/camping-resort-almafra",
    ),
]


def create_family_camping_post(apps, schema_editor):
    Post = apps.get_model("blog", "Post")
    User = apps.get_model("auth", "User")

    if Post.objects.filter(slug=POST_SLUG).exists():
        return

    author = User.objects.filter(is_superuser=True).order_by("id").first() or User.objects.order_by("id").first()
    if not author:
        return

    sections = []
    for index, (name, location, description, destination) in enumerate(CAMPINGS, start=1):
        sections.append(
            f'''<h2>{index}. {name}</h2>
<p><strong>{location}.</strong> {description}</p>
<p><a href="{awin(destination)}" target="_blank" rel="nofollow sponsored noopener"><strong>Ver disponibilidad y precios de {name} →</strong></a></p>'''
        )

    content = f'''
<p>Viajar de camping con niños cambia bastante la lista de prioridades. La piscina importa, pero también el club infantil, las actividades, la cercanía a la playa o a lugares que permitan improvisar un plan familiar sin pasar media jornada en carretera.</p>
<p>Hemos seleccionado siete campings de España que reúnen varios de esos ingredientes. No se trata de elegir un ganador absoluto, sino de ayudarte a encontrar el que encaje mejor con la edad de los niños, la época del viaje y el tipo de vacaciones que buscas.</p>
{''.join(sections)}
<h2>¿Qué mirar antes de reservar un camping con niños?</h2>
<p>Comprueba las fechas de apertura de piscinas, clubes infantiles y programas de animación, porque algunos servicios son estacionales. También conviene revisar la distancia real a la playa, el tipo de alojamiento o parcela, la sombra disponible y las normas del camping.</p>
<p>Si viajas en camper, caravana o autocaravana, revisa además las dimensiones admitidas, la conexión eléctrica y los servicios de agua y vaciado antes de reservar.</p>
<p><strong>¿Preparando el viaje?</strong> Puedes consultar también nuestra <a href="/shop/"><strong>selección de equipamiento camper y camping →</strong></a> y la guía de <a href="/blog/escapada-fin-de-semana-autocaravana/"><strong>qué llevar para una escapada en autocaravana</strong></a>.</p>
<hr>
<p><small>Este artículo contiene enlaces de afiliado. Si reservas a través de alguno de ellos, Caravaning Project puede recibir una comisión sin coste adicional para ti. Los servicios, actividades, precios y disponibilidad pueden cambiar, por lo que recomendamos comprobar la información actual antes de reservar.</small></p>
'''.strip()

    Post.objects.create(
        slug=POST_SLUG,
        title="Campings para ir con niños en España: 7 opciones para unas vacaciones en familia",
        content=content,
        meta_description="7 campings para ir con niños en España con piscinas, animación, clubes infantiles, playa y naturaleza para preparar unas vacaciones en familia.",
        status="PUBLISHED",
        author=author,
    )


class Migration(migrations.Migration):
    dependencies = [
        ("blog", "0071_reforzar_escapada_fin_semana_monetizacion"),
    ]

    operations = [
        migrations.RunPython(create_family_camping_post, migrations.RunPython.noop),
    ]
