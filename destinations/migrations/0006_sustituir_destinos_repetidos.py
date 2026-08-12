from django.db import migrations

OLD_TITLES = [
    "Picos de Europa: montaña, lagos y rutas para viajar en camper",
    "Delta del Ebro: arrozales, playas y naturaleza en camper",
    "Las Médulas: un paisaje único entre montañas y antiguas minas romanas",
    "Sierra de Cazorla: naturaleza y carreteras panorámicas en autocaravana",
    "Cap de Creus: la Costa Brava más salvaje",
]

NEW_DESTINATIONS = [
    {
        "title": "Parque Nacional de Monfragüe: naturaleza salvaje en Extremadura",
        "location": "Monfragüe, Cáceres, Extremadura",
        "image_url": "https://commons.wikimedia.org/wiki/Special:FilePath/Monfrague%20National%20Park.jpg",
        "description": "<p>El <strong>Parque Nacional de Monfragüe</strong> es uno de los grandes espacios naturales de Extremadura y un destino especialmente interesante para quienes disfrutan de la observación de aves, los bosques mediterráneos y las rutas tranquilas.</p><p>Para viajar en camper o autocaravana conviene utilizar campings y áreas autorizadas de los municipios del entorno y desplazarse hasta los miradores y rutas respetando la normativa del parque.</p><p><strong>Ideal para:</strong> naturaleza, fotografía, aves, senderismo y escapadas de primavera y otoño.</p>",
    },
    {
        "title": "Sierra de Albarracín: pueblos de piedra y bosques de Teruel",
        "location": "Sierra de Albarracín, Teruel, Aragón",
        "image_url": "https://commons.wikimedia.org/wiki/Special:FilePath/Albarracin%20Spain.jpg",
        "description": "<p>La <strong>Sierra de Albarracín</strong> combina pueblos históricos, pinares, barrancos y carreteras de montaña en uno de los rincones más sorprendentes de Teruel.</p><p>Albarracín es una excelente base para una ruta en camper, pero merece la pena ampliar el recorrido hacia los paisajes naturales de la sierra y organizar las noches en campings o espacios autorizados.</p><p><strong>Ideal para:</strong> pueblos, senderismo, fotografía, gastronomía y rutas de montaña.</p>",
    },
    {
        "title": "Parque Nacional de Cabañeros: la gran naturaleza del centro de España",
        "location": "Cabañeros, Ciudad Real y Toledo, Castilla-La Mancha",
        "image_url": "https://commons.wikimedia.org/wiki/Special:FilePath/Cabaneros%20National%20Park.jpg",
        "description": "<p>El <strong>Parque Nacional de Cabañeros</strong> ofrece un paisaje de rañas, monte mediterráneo y sierras que resulta especialmente atractivo fuera de los meses de mayor calor.</p><p>Es un destino estupendo para combinar una ruta en autocaravana con visitas guiadas, observación de fauna y pueblos de los Montes de Toledo. Para pernoctar, utiliza instalaciones y áreas autorizadas del entorno.</p><p><strong>Ideal para:</strong> fauna, fotografía, naturaleza, rutas tranquilas y escapadas de otoño.</p>",
    },
    {
        "title": "Parque Natural de Somiedo: lagos, brañas y montaña asturiana",
        "location": "Somiedo, Asturias",
        "image_url": "https://commons.wikimedia.org/wiki/Special:FilePath/Somiedo%20Asturias.jpg",
        "description": "<p>El <strong>Parque Natural de Somiedo</strong> es uno de los grandes paisajes de montaña de Asturias, con lagos, valles, bosques y las tradicionales brañas.</p><p>Es una opción fantástica para una ruta en camper o autocaravana por el interior asturiano. Antes de entrar en zonas protegidas, consulta las restricciones de circulación, estacionamiento y pernocta y utiliza los lugares autorizados.</p><p><strong>Ideal para:</strong> montaña, senderismo, fotografía, gastronomía y viajes en primavera y otoño.</p>",
    },
    {
        "title": "Sierra de Aracena y Picos de Aroche: dehesas y pueblos blancos",
        "location": "Sierra de Aracena, Huelva, Andalucía",
        "image_url": "https://commons.wikimedia.org/wiki/Special:FilePath/Aracena%20Huelva%20Spain.jpg",
        "description": "<p>La <strong>Sierra de Aracena y Picos de Aroche</strong> es una alternativa perfecta para descubrir una Andalucía diferente: dehesas, castañares, pueblos blancos, senderos y una gastronomía con enorme personalidad.</p><p>La zona funciona muy bien para una escapada en camper o autocaravana, especialmente en otoño, cuando los bosques y pueblos adquieren un ambiente espectacular. Planifica las pernoctas en campings y áreas autorizadas.</p><p><strong>Ideal para:</strong> gastronomía, pueblos, senderismo, naturaleza y escapadas de otoño.</p>",
    },
]


def replace_destinations(apps, schema_editor):
    Destination = apps.get_model("destinations", "Destination")
    User = apps.get_model("auth", "User")
    author = User.objects.filter(username="miguel").first() or User.objects.filter(is_superuser=True).first()
    if not author:
        return

    # Elimina los cinco destinos introducidos por 0005, tanto si la migración
    # anterior ya se ejecutó como si acaba de ejecutarse en esta migración.
    Destination.objects.filter(title__in=OLD_TITLES).delete()

    for data in NEW_DESTINATIONS:
        Destination.objects.update_or_create(
            title=data["title"],
            defaults={
                "author": author,
                "location": data["location"],
                "description": data["description"],
                "image_url": data["image_url"],
            },
        )


def restore_old_destinations(apps, schema_editor):
    Destination = apps.get_model("destinations", "Destination")
    Destination.objects.filter(title__in=[d["title"] for d in NEW_DESTINATIONS]).delete()


class Migration(migrations.Migration):
    dependencies = [("destinations", "0005_nuevos_destinos")]
    operations = [migrations.RunPython(replace_destinations, restore_old_destinations)]
