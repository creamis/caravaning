from django.db import migrations

DESTINATIONS = [
    {"title": "Picos de Europa: montaña, lagos y rutas para viajar en camper", "location": "Picos de Europa, Asturias, Cantabria y León", "image_url": "https://commons.wikimedia.org/wiki/Special:FilePath/PICOS%20DE%20EUROPA%201.jpg", "description": "<p>Los <strong>Picos de Europa</strong> son una de las grandes escapadas de montaña del norte de España. El Parque Nacional se extiende por Asturias, Cantabria y Castilla y León, con montañas, valles, pueblos y rutas espectaculares.</p><p>Para viajar en camper o autocaravana conviene utilizar campings y áreas autorizadas y consultar las restricciones del parque y de cada municipio. Lagos de Covadonga, Fuente Dé, Poncebos y Cangas de Onís permiten organizar rutas muy diferentes.</p><p><strong>Ideal para:</strong> senderismo, naturaleza, fotografía y escapadas de varios días.</p>"},
    {"title": "Delta del Ebro: arrozales, playas y naturaleza en camper", "location": "Delta del Ebro, Tarragona, Cataluña", "image_url": "https://commons.wikimedia.org/wiki/Special:FilePath/Arrozales%20en%20el%20Delta.jpg", "description": "<p>El <strong>Delta del Ebro</strong> ofrece un paisaje de arrozales, lagunas, playas y una enorme variedad de aves en uno de los humedales más importantes del Mediterráneo occidental.</p><p>Es un destino especialmente interesante para recorrer en camper, combinando pequeñas carreteras, Deltebre, Sant Carles de la Ràpita y rutas en bicicleta. Para pernoctar hay que utilizar establecimientos y espacios autorizados y respetar la normativa del Parque Natural.</p><p><strong>Ideal para:</strong> bicicleta, naturaleza, fotografía, gastronomía y escapadas junto al Mediterráneo.</p>"},
    {"title": "Las Médulas: un paisaje único entre montañas y antiguas minas romanas", "location": "Las Médulas, León, Castilla y León", "image_url": "https://commons.wikimedia.org/wiki/Special:FilePath/As%20Medulas%20gold%20mine%20of%20the%20Romans.jpg", "description": "<p><strong>Las Médulas</strong> es uno de esos lugares que parecen sacados de otro planeta. Las antiguas explotaciones mineras romanas crearon un paisaje de montañas rojizas, bosques y senderos que hoy forman parte del Patrimonio Mundial de la UNESCO.</p><p>Es una buena parada para una ruta en autocaravana o camper por León y El Bierzo. Puedes combinar miradores y senderos con pueblos, gastronomía y otros espacios naturales de la comarca.</p><p><strong>Ideal para:</strong> senderismo, historia, fotografía y viajes tranquilos por el noroeste.</p>"},
    {"title": "Sierra de Cazorla: naturaleza y carreteras panorámicas en autocaravana", "location": "Sierra de Cazorla, Jaén, Andalucía", "image_url": "https://commons.wikimedia.org/wiki/Special:FilePath/Cazorla%2C%20Spain.jpg", "description": "<p>La <strong>Sierra de Cazorla, Segura y Las Villas</strong> es una magnífica opción para descubrir la Andalucía interior. Bosques, ríos, miradores y pueblos de montaña permiten organizar una ruta pausada en camper o autocaravana.</p><p>El río Borosa, el nacimiento del Guadalquivir y Cazorla ofrecen diferentes planes para varios días. En los espacios protegidos es especialmente importante respetar las zonas de estacionamiento y pernocta autorizadas.</p><p><strong>Ideal para:</strong> naturaleza, senderismo, fotografía, gastronomía y rutas de montaña.</p>"},
    {"title": "Cap de Creus: la Costa Brava más salvaje", "location": "Cap de Creus, Girona, Cataluña", "image_url": "https://commons.wikimedia.org/wiki/Special:FilePath/Cap%20de%20Creus%2C%20Catalonia.jpg", "description": "<p>El <strong>Cap de Creus</strong> es uno de los paisajes costeros más singulares de Cataluña. La roca, el Mediterráneo, pequeñas calas y carreteras del Alt Empordà convierten la zona en una escapada fantástica.</p><p>Cadaqués, Portlligat y el parque natural permiten combinar mar, senderismo y cultura. Si viajas en camper o autocaravana, planifica la ruta y utiliza únicamente las zonas permitidas para estacionar y pernoctar.</p><p><strong>Ideal para:</strong> costa, senderismo, fotografía, pueblos mediterráneos y escapadas fuera de temporada.</p>"},
]


def add_destinations(apps, schema_editor):
    Destination = apps.get_model("destinations", "Destination")
    User = apps.get_model("auth", "User")
    author = User.objects.filter(username="miguel").first() or User.objects.filter(is_superuser=True).first()
    if not author:
        return
    for data in DESTINATIONS:
        if not Destination.objects.filter(title=data["title"]).exists():
            Destination.objects.create(author=author, **data)


def remove_destinations(apps, schema_editor):
    Destination = apps.get_model("destinations", "Destination")
    Destination.objects.filter(title__in=[d["title"] for d in DESTINATIONS]).delete()


class Migration(migrations.Migration):
    dependencies = [("destinations", "0004_destination_image_url_destinationimage_image_url_and_more")]
    operations = [migrations.RunPython(add_destinations, remove_destinations)]
