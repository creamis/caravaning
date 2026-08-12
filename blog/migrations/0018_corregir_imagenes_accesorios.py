import re
from django.db import migrations

POST_SLUG = "20-accesorios-imprescindibles-camper-menos-50-euros"

# Imágenes corregidas para que cada apartado muestre el objeto que corresponde.
# Todas proceden de Wikimedia Commons y se mantienen como URL externas.
CORRECTED = {
    7: ("Papelera / cubo de residuos compacto", "https://commons.wikimedia.org/wiki/Special:Redirect/file/Trash_cans.jpg"),
    8: ("Cajas y organizadores de almacenamiento", "https://commons.wikimedia.org/wiki/Special:Redirect/file/Plasmid_Storage_Box.jpg"),
    9: ("Organizador o estantería para zapatos", "https://commons.wikimedia.org/wiki/Special:Redirect/file/Shoe_Rack_in_masjid.jpg"),
    10: ("Set de cocina compacto de aluminio", "https://commons.wikimedia.org/wiki/Special:Redirect/file/Ali1234.jpg"),
    12: ("Botella reutilizable para agua", "https://commons.wikimedia.org/wiki/Special:Redirect/file/WaterBottle.jpg"),
    13: ("Ducha portátil para camping", "https://commons.wikimedia.org/wiki/Special:Redirect/file/Camping_showers_(4613626640).jpg"),
    14: ("Mesa plegable", "https://commons.wikimedia.org/wiki/Special:Redirect/file/Folding_table.jpg"),
    15: ("Ganchos para organizar cables y pequeños accesorios", "https://commons.wikimedia.org/wiki/Special:Redirect/file/Cable_hooks.jpg"),
    16: ("Tendedero para ropa", "https://commons.wikimedia.org/wiki/Special:Redirect/file/Clothesline_(9459404442).jpg"),
    17: ("Detector de monóxido de carbono", "https://commons.wikimedia.org/wiki/Special:Redirect/file/Carbon_monoxide_detector.jpg"),
    18: ("Kit completo de herramientas", "https://commons.wikimedia.org/wiki/Special:Redirect/file/Repair_tool_kit.jpg"),
    20: ("Kit de reparación", "https://commons.wikimedia.org/wiki/Special:Redirect/file/Repair_kit.jpg"),
}


def replace_nth_image(content, n, url):
    count = 0

    def repl(match):
        nonlocal count
        count += 1
        if count == n:
            return match.group(1) + url + match.group(3)
        return match.group(0)

    return re.sub(r'(<img\s+[^>]*?src=[\"\'])(.*?)([\"\'])', repl, content, flags=re.IGNORECASE)


def correct_images(apps, schema_editor):
    Post = apps.get_model("blog", "Post")
    PostImage = apps.get_model("blog", "PostImage")

    post = Post.objects.filter(slug=POST_SLUG).first()
    if not post:
        return

    # Corregimos exactamente las imágenes 7, 8, 9, 10, 12, 13, 14, 15, 16, 17, 18 y 20.
    for number, (_name, url) in CORRECTED.items():
        post.content = replace_nth_image(post.content, number, url)

    # Ajustamos también los títulos de los apartados para que no haya contradicción
    # con la fotografía mostrada.
    replacements = {
        "<h2>7. Papelera plegable</h2>": "<h2>7. Papelera / cubo de residuos compacto</h2>",
        "<h2>8. Organizadores de almacenamiento</h2>": "<h2>8. Organizadores de almacenamiento</h2>",
        "<h2>9. Organizador para zapatos</h2>": "<h2>9. Organizador para zapatos</h2>",
        "<h2>10. Set de cocina compacto</h2>": "<h2>10. Set de cocina compacto</h2>",
    }
    for old, new in replacements.items():
        post.content = post.content.replace(old, new)

    post.save(update_fields=["content", "updated_at"])

    # La galería/carrusel debe utilizar exactamente las mismas imágenes que el artículo.
    PostImage.objects.filter(post=post).delete()

    cover = "https://commons.wikimedia.org/wiki/Special:Redirect/file/Volkswagen-Combi-T2-Adventure-Awaits-byRundvald.jpg"
    PostImage.objects.create(post=post, image_url=cover)

    # Extraemos las URLs de las 20 imágenes del contenido para mantener una única fuente de verdad.
    urls = re.findall(r'<img\s+[^>]*?src=[\"\'](.*?)[\"\']', post.content, flags=re.IGNORECASE)
    for url in urls[:20]:
        PostImage.objects.get_or_create(post=post, image_url=url)

    credits = """
<h3>📷 Fotografías corregidas</h3>
<p>Para estos apartados se han sustituido las imágenes que no correspondían al producto por fotografías específicas del objeto mostrado. Las fuentes proceden de Wikimedia Commons y sus páginas de archivo indican las licencias de reutilización correspondientes.</p>
<p><a href="https://commons.wikimedia.org/wiki/File:Trash_cans.jpg" target="_blank" rel="noopener">Papelera</a> · <a href="https://commons.wikimedia.org/wiki/File:Plasmid_Storage_Box.jpg" target="_blank" rel="noopener">Caja de almacenamiento</a> · <a href="https://commons.wikimedia.org/wiki/File:Shoe_Rack_in_masjid.jpg" target="_blank" rel="noopener">Zapatero</a> · <a href="https://commons.wikimedia.org/wiki/File:Ali1234.jpg" target="_blank" rel="noopener">Set de cocina</a> · <a href="https://commons.wikimedia.org/wiki/File:WaterBottle.jpg" target="_blank" rel="noopener">Botella</a> · <a href="https://commons.wikimedia.org/wiki/File:Camping_showers_(4613626640).jpg" target="_blank" rel="noopener">Ducha de camping</a> · <a href="https://commons.wikimedia.org/wiki/File:Folding_table.jpg" target="_blank" rel="noopener">Mesa plegable</a> · <a href="https://commons.wikimedia.org/wiki/File:Cable_hooks.jpg" target="_blank" rel="noopener">Ganchos</a> · <a href="https://commons.wikimedia.org/wiki/File:Clothesline_(9459404442).jpg" target="_blank" rel="noopener">Tendedero</a> · <a href="https://commons.wikimedia.org/wiki/File:Carbon_monoxide_detector.jpg" target="_blank" rel="noopener">Detector de CO</a> · <a href="https://commons.wikimedia.org/wiki/File:Repair_tool_kit.jpg" target="_blank" rel="noopener">Herramientas</a> · <a href="https://commons.wikimedia.org/wiki/File:Repair_kit.jpg" target="_blank" rel="noopener">Kit de reparación</a>.</p>
"""
    marker = "<h3>📷 Fotografías corregidas</h3>"
    if marker not in post.content:
        post.content += credits
        post.save(update_fields=["content", "updated_at"])


def reverse_correct_images(apps, schema_editor):
    pass


class Migration(migrations.Migration):
    dependencies = [("blog", "0017_fotos_productos_reales_cc")]
    operations = [migrations.RunPython(correct_images, reverse_correct_images)]
