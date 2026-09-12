from django.db import migrations
from urllib.parse import quote

POST_SLUG = "mejores-campings-playa-espana-camper-caravana-autocaravana"
AWIN_MID = "13054"
AWIN_AFFID = "2917197"


def awin(destination):
    return (
        "https://www.awin1.com/cread.php?"
        f"awinmid={AWIN_MID}&awinaffid={AWIN_AFFID}&ued={quote(destination, safe='')}"
    )


CAMPINGS = [
    (
        "Camping Playa Brava - Pals (Girona)",
        "https://es.camping-and-co.com/camping-playa-brava",
        "A solo unos metros de la playa de Pals, en plena Costa Brava. Es una opción especialmente atractiva para combinar Mediterráneo, naturaleza y excursiones por pueblos del Empordà como Pals, Peratallada o Palafrugell.",
    ),
    (
        "Camping Torre de la Mora - Tarragona",
        "https://es.camping-and-co.com/camping-torre-de-la-mora",
        "Una alternativa de Costa Dorada con acceso prácticamente directo al mar. Su situación permite combinar días de playa con Tarragona y otros planes de la costa catalana.",
    ),
    (
        "Camping Treumal - Platja d'Aro (Girona)",
        "https://es.camping-and-co.com/camping-treumal",
        "Situado junto a la playa de Can Cristus, es una opción muy interesante para quienes quieren tener el mar como protagonista y utilizar el camping como base para recorrer la Costa Brava.",
    ),
    (
        "Camping Platja Cambrils - Cambrils (Tarragona)",
        "https://es.camping-and-co.com/camping-playa-cambrils",
        "Muy cerca de la playa y bien situado para conocer Cambrils y la Costa Dorada. También permite combinar la estancia con excursiones y planes familiares por la provincia de Tarragona.",
    ),
    (
        "Camping La Sirena - L'Estartit (Girona)",
        "https://es.camping-and-co.com/camping-la-sirena",
        "Una opción costera en L'Estartit, junto al entorno natural del Ter Vell y muy cerca de la playa. Encaja especialmente bien para combinar mar, naturaleza y excursiones por esta zona de la Costa Brava.",
    ),
    (
        "Camping Playa y Fiesta - Mont-roig del Camp (Tarragona)",
        "https://es.camping-and-co.com/camping-playa-y-fiesta",
        "Situado en la Costa Dorada y a poca distancia del mar, ofrece una base costera para disfrutar de la playa y recorrer localidades del litoral de Tarragona.",
    ),
    (
        "Camping Alegria del Mar - Benicarló (Castellón)",
        "https://es.camping-and-co.com/camping-alegria-del-mar",
        "Situado junto al Mediterráneo en Benicarló, es una alternativa interesante para ampliar la ruta hacia la costa de Castellón. Su cercanía al mar permite combinar playa con escapadas por el litoral y localidades próximas como Peñíscola.",
    ),
]


def build_content():
    parts = [
        "<h2>7 campings de playa en España para camper, caravana o autocaravana</h2>",
        "<p>Despertarse cerca del Mediterráneo, desayunar al aire libre y tener la playa a pocos minutos es uno de los grandes atractivos de viajar de camping. En esta selección reunimos siete establecimientos costeros que cuentan con ficha en Camping &amp; Co y que pueden servir como punto de partida para preparar unas vacaciones junto al mar.</p>",
        "<p><strong>Antes de reservar:</strong> comprueba siempre las fechas, el tipo de alojamiento o parcela disponible y las condiciones para caravanas, campers o autocaravanas. La disponibilidad cambia según temporada y establecimiento.</p>",
    ]

    for index, (name, destination, description) in enumerate(CAMPINGS, start=1):
        parts.extend([
            f"<h3>{index}. {name}</h3>",
            f"<p>{description}</p>",
            f'<p><a href="{awin(destination)}" target="_blank" rel="nofollow sponsored noopener"><strong>Ver precios y disponibilidad en Camping &amp; Co →</strong></a></p>',
        ])

    all_spain = awin("https://es.camping-and-co.com/vacaciones-camping-en-espana")
    parts.extend([
        "<h3>Qué revisar al elegir un camping junto a la playa</h3>",
        "<p>La distancia al mar es importante, pero no debería ser el único criterio. Si viajas con vehículo vivienda revisa también el acceso, las dimensiones de la parcela, conexiones eléctricas y de agua, sombra, servicios de vaciado cuando correspondan y las normas específicas del establecimiento.</p>",
        "<p>En temporada alta también merece la pena comparar fechas. Un mismo camping puede tener disponibilidad una semana y aparecer completo la siguiente, y Camping &amp; Co puede mostrar alternativas cercanas cuando el establecimiento elegido no dispone de plazas para la búsqueda realizada.</p>",
        f'<p><a href="{all_spain}" target="_blank" rel="nofollow sponsored noopener"><strong>🏕️ Explorar más campings en España en Camping &amp; Co</strong></a></p>',
        "<hr>",
        "<p><small>Este artículo contiene enlaces de afiliado. Si realizas una reserva a través de alguno de ellos, Caravaning Project puede recibir una comisión sin coste adicional para ti.</small></p>",
    ])
    return "\n".join(parts)


CONTENT = build_content()


def create_post(apps, schema_editor):
    Post = apps.get_model("blog", "Post")
    User = apps.get_model("auth", "User")

    post = Post.objects.filter(slug=POST_SLUG).first()
    if not post:
        author = User.objects.filter(is_superuser=True).order_by("id").first()
        if not author:
            author = User.objects.order_by("id").first()
        if not author:
            return
        Post.objects.create(
            slug=POST_SLUG,
            title="7 campings de playa en España para camper, caravana o autocaravana",
            content=CONTENT,
            meta_description="Descubre 7 campings de playa en España para preparar una escapada en camper, caravana o autocaravana por la Costa Brava, Costa Dorada y el Mediterráneo.",
            status="PUBLISHED",
            author=author,
        )
        return

    post.title = "7 campings de playa en España para camper, caravana o autocaravana"
    post.content = CONTENT
    post.meta_description = "Descubre 7 campings de playa en España para preparar una escapada en camper, caravana o autocaravana por la Costa Brava, Costa Dorada y el Mediterráneo."
    post.status = "PUBLISHED"
    post.save(update_fields=["title", "content", "meta_description", "status"])


class Migration(migrations.Migration):
    dependencies = [
        ("blog", "0059_imagenes_campings_espana_camping_and_co"),
    ]

    operations = [
        migrations.RunPython(create_post, migrations.RunPython.noop),
    ]
