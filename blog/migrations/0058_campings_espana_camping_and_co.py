from django.db import migrations
from urllib.parse import quote

POST_SLUG = "mejores-campings-espana-camper-caravana-autocaravana"
AWIN_MID = "13054"
AWIN_AFFID = "2917197"


def awin(destination):
    return (
        "https://www.awin1.com/cread.php?"
        f"awinmid={AWIN_MID}&awinaffid={AWIN_AFFID}&ued={quote(destination, safe='')}"
    )


CAMPINGS = [
    (
        "Camping Costa Blanca - El Campello (Alicante)",
        "https://es.camping-and-co.com/camping-costa-blanca",
        "Una opción mediterránea muy interesante para combinar camping, playa y visitas por la Costa Blanca. El Campello está bien situado para descubrir Alicante y otras localidades costeras.",
    ),
    (
        "Camping Cabo de Gata - Almería",
        "https://es.camping-and-co.com/camping-cabo-de-gata",
        "Una base estupenda para descubrir el Parque Natural de Cabo de Gata-Níjar y disfrutar de una escapada en la que el paisaje, las playas y las rutas tienen todo el protagonismo.",
    ),
    (
        "Camping L'Amfora - Sant Pere Pescador (Girona)",
        "https://es.camping-and-co.com/camping-l-amfora",
        "Situado en la Costa Brava y junto al golfo de Roses, encaja especialmente bien en viajes que mezclan playa, naturaleza y excursiones por el Empordà.",
    ),
    (
        "King's Camping - Palamós (Girona)",
        "https://es.camping-and-co.com/camping-kings-camping",
        "Una alternativa en Palamós para disfrutar de la Costa Brava, con playa cercana y un entorno adecuado para unas vacaciones de camping junto al Mediterráneo.",
    ),
    (
        "Camping Huttopia Parque de Doñana - Hinojos (Huelva)",
        "https://es.camping-and-co.com/camping-parque-de-donana",
        "Para quienes prefieren naturaleza y tranquilidad, su entorno de pinares y la proximidad de Doñana lo convierten en un punto de partida muy atractivo para conocer esta zona de Andalucía.",
    ),
    (
        "Camping Valle Niza Playa - Málaga",
        "https://es.camping-and-co.com/campeggio-valle-niza-playa",
        "Una propuesta de Costa del Sol que combina mar y montaña, especialmente interesante para quienes buscan una estancia cerca de la playa y quieren recorrer la costa malagueña.",
    ),
]


def build_content():
    parts = [
        "<h2>6 campings en España para una escapada en camper, caravana o autocaravana</h2>",
        "<p>España ofrece opciones de camping muy diferentes: costa mediterránea, espacios naturales, playas y destinos de montaña. En esta selección reunimos seis campings disponibles en Camping &amp; Co que pueden servirte como punto de partida para preparar una próxima escapada.</p>",
        "<p><strong>Importante:</strong> antes de reservar, comprueba siempre en la ficha del establecimiento las condiciones de acceso, el tipo de alojamiento o parcela disponible y si admite específicamente tu tipo de vehículo.</p>",
    ]

    for index, (name, destination, description) in enumerate(CAMPINGS, start=1):
        affiliate = awin(destination)
        parts.extend([
            f"<h3>{index}. {name}</h3>",
            f"<p>{description}</p>",
            f'<p><a href="{affiliate}" target="_blank" rel="nofollow sponsored noopener"><strong>Ver camping y disponibilidad en Camping &amp; Co →</strong></a></p>',
        ])

    all_spain = awin("https://es.camping-and-co.com/vacaciones-camping-en-espana")
    parts.extend([
        "<h3>Cómo elegir el camping adecuado</h3>",
        "<p>Si viajas con camper, caravana o autocaravana, no te fijes únicamente en el destino. Revisa el acceso, dimensiones y características de la parcela, conexiones eléctricas, puntos de agua, servicios de vaciado cuando proceda, normas para mascotas y distancia a los lugares que quieras visitar.</p>",
        "<p>La disponibilidad y las modalidades de estancia pueden cambiar según fechas y establecimiento, así que conviene comprobar la información actualizada antes de hacer la reserva.</p>",
        f'<p><a href="{all_spain}" target="_blank" rel="nofollow sponsored noopener"><strong>🏕️ Ver más campings en España en Camping &amp; Co</strong></a></p>',
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
            title="6 campings en España para una escapada en camper, caravana o autocaravana",
            content=CONTENT,
            meta_description="Descubre 6 campings en España para preparar una escapada en camper, caravana o autocaravana, con opciones de costa y naturaleza.",
            status="PUBLISHED",
            author=author,
        )
        return

    post.title = "6 campings en España para una escapada en camper, caravana o autocaravana"
    post.content = CONTENT
    post.meta_description = "Descubre 6 campings en España para preparar una escapada en camper, caravana o autocaravana, con opciones de costa y naturaleza."
    post.status = "PUBLISHED"
    post.save(update_fields=["title", "content", "meta_description", "status"])


class Migration(migrations.Migration):
    dependencies = [
        ("blog", "0057_cambiar_imagenes_2_3_escapada_autocaravana"),
    ]

    operations = [
        migrations.RunPython(create_post, migrations.RunPython.noop),
    ]
