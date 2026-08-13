from django.db import migrations

IMAGE_FIXES = {
    "Parque Nacional de Monfragüe: naturaleza salvaje en Extremadura":
        "https://commons.wikimedia.org/wiki/Special:FilePath/Monfrague%201.jpg",
    "Sierra de Albarracín: pueblos de piedra y bosques de Teruel":
        "https://commons.wikimedia.org/wiki/Special:FilePath/Albarracin%2C%20Spain.jpg",
    "Parque Nacional de Cabañeros: la gran naturaleza del centro de España":
        "https://commons.wikimedia.org/wiki/Special:FilePath/Dehesa%20cabaneros.jpg",
    "Parque Natural de Somiedo: lagos, brañas y montaña asturiana":
        "https://commons.wikimedia.org/wiki/Special:FilePath/Lagos%20de%20Saliencia%20en%20el%20Parque%20Natural%20de%20Somiedo%20Asturias.jpg",
    "Sierra de Aracena y Picos de Aroche: dehesas y pueblos blancos":
        "https://commons.wikimedia.org/wiki/Special:FilePath/Aracena%20-%20Paisaje%2001.jpg",
}


def fix_images(apps, schema_editor):
    Destination = apps.get_model("destinations", "Destination")
    for title, image_url in IMAGE_FIXES.items():
        Destination.objects.filter(title=title).update(image_url=image_url, image=None)


def reverse_fix(apps, schema_editor):
    Destination = apps.get_model("destinations", "Destination")
    Destination.objects.filter(title__in=IMAGE_FIXES.keys()).update(image_url=None)


class Migration(migrations.Migration):
    dependencies = [("destinations", "0006_sustituir_destinos_repetidos")]
    operations = [migrations.RunPython(fix_images, reverse_fix)]
