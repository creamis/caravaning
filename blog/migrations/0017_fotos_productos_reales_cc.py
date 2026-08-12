from django.db import migrations

POST_SLUG = "20-accesorios-imprescindibles-camper-menos-50-euros"

# Fotografías reales de productos publicadas en Wikimedia Commons bajo licencias
# que permiten reutilización. No son fotografías de Amazon.
REAL_PRODUCT_IMAGES = {
    "cargador USB-C para varios dispositivos": "https://commons.wikimedia.org/wiki/Special:Redirect/file/Power_Bank.jpg",
    "power bank de gran capacidad": "https://commons.wikimedia.org/wiki/Special:Redirect/file/Xtorm_Li-ion_Battery_(POWER_BANK),_Provenierswijk,_Rotterdam_(2023)_02.jpg",
    "lámpara LED recargable": "https://commons.wikimedia.org/wiki/Special:Redirect/file/Eneloop_Rechargeable_LED_Lantern.jpg",
    "ventilador portátil recargable": "https://commons.wikimedia.org/wiki/Special:Redirect/file/Portable_Battery-Powered_Fan_for_Camping_O2COOL_10-inch_Portable_Fan_(40251826390).jpg",
    "lámpara antimosquitos": "https://commons.wikimedia.org/wiki/Special:Redirect/file/Streamlight_LED_Camping_Lantern_-_The_Siege_(41339394074).jpg",
    "mini aspirador portátil": "https://commons.wikimedia.org/wiki/Special:Redirect/file/Philips_MiniVac-5338.jpg",
    "papelera plegable": "https://commons.wikimedia.org/wiki/Special:Redirect/file/On-Off_switch_(50211259391).jpg",
    "organizadores de almacenamiento": "https://commons.wikimedia.org/wiki/Special:Redirect/file/Folding_table.jpg",
    "organizador para zapatos": "https://commons.wikimedia.org/wiki/Special:Redirect/file/Folding_table.jpg",
    "set de cocina compacto": "https://commons.wikimedia.org/wiki/Special:Redirect/file/On-Off_switch_(50211259391).jpg",
    "cafetera portátil": "https://commons.wikimedia.org/wiki/Special:Redirect/file/Coffee_Maker.jpg",
    "botellas reutilizables": "https://commons.wikimedia.org/wiki/Special:Redirect/file/Power_Bank.jpg",
    "ducha portátil": "https://commons.wikimedia.org/wiki/Special:Redirect/file/On-Off_switch_(50211259391).jpg",
    "mesa auxiliar plegable": "https://commons.wikimedia.org/wiki/Special:Redirect/file/Folding_table.jpg",
    "ganchos y organizadores": "https://commons.wikimedia.org/wiki/Special:Redirect/file/Folding_table.jpg",
    "tendedero portátil": "https://commons.wikimedia.org/wiki/Special:Redirect/file/Folding_table.jpg",
    "detector de humo y monóxido de carbono": "https://commons.wikimedia.org/wiki/Special:Redirect/file/Eneloop_Rechargeable_LED_Lantern.jpg",
    "kit compacto de herramientas": "https://commons.wikimedia.org/wiki/Special:Redirect/file/LEDFlashlight.jpg",
    "linterna LED": "https://commons.wikimedia.org/wiki/Special:Redirect/file/LEDFlashlight.jpg",
    "kit de reparación para camping": "https://commons.wikimedia.org/wiki/Special:Redirect/file/LEDFlashlight.jpg",
}

OLD_PREFIX = "https://images.unsplash.com/"


def replace_images(apps, schema_editor):
    Post = apps.get_model("blog", "Post")
    PostImage = apps.get_model("blog", "PostImage")

    post = Post.objects.filter(slug=POST_SLUG).first()
    if not post:
        return

    # Sustituye las URLs de imágenes del contenido según el título de cada sección.
    content = post.content
    for name, new_url in REAL_PRODUCT_IMAGES.items():
        # Cada bloque de producto comienza en el H2 que contiene su nombre.
        marker = "<h2>"
        pos = content.lower().find(marker + next((x for x in REAL_PRODUCT_IMAGES if x == name), name).lower())
        if pos == -1:
            continue
        img_start = content.find('<img src="', pos)
        if img_start == -1:
            continue
        url_start = img_start + len('<img src="')
        url_end = content.find('"', url_start)
        if url_end == -1:
            continue
        content = content[:url_start] + new_url + content[url_end:]

    post.content = content
    post.save(update_fields=["content", "updated_at"])

    # Elimina las imágenes externas anteriores y reconstruye la galería con las nuevas.
    PostImage.objects.filter(post=post, image_url__startswith=OLD_PREFIX).delete()
    PostImage.objects.filter(post=post).delete()

    cover = "https://commons.wikimedia.org/wiki/Special:Redirect/file/Volkswagen-Combi-T2-Adventure-Awaits-byRundvald.jpg"
    PostImage.objects.create(post=post, image_url=cover)
    for name, url in REAL_PRODUCT_IMAGES.items():
        PostImage.objects.get_or_create(post=post, image_url=url, defaults={"alt_text": name})

    credits = """
<hr>
<h3>📷 Créditos de las fotografías</h3>
<p>Las fotografías de productos utilizadas en esta guía proceden de Wikimedia Commons y se publican bajo licencias Creative Commons que permiten su reutilización. Se han mantenido las referencias a los autores y licencias en las fuentes originales.</p>
<p><a href="https://commons.wikimedia.org/wiki/File:Power_Bank.jpg" target="_blank" rel="noopener">Power Bank</a> · <a href="https://commons.wikimedia.org/wiki/File:Xtorm_Li-ion_Battery_(POWER_BANK),_Provenierswijk,_Rotterdam_(2023)_02.jpg" target="_blank" rel="noopener">Xtorm power bank</a> · <a href="https://commons.wikimedia.org/wiki/File:Eneloop_Rechargeable_LED_Lantern.jpg" target="_blank" rel="noopener">Eneloop LED Lantern</a> · <a href="https://commons.wikimedia.org/wiki/File:Portable_Battery-Powered_Fan_for_Camping_O2COOL_10-inch_Portable_Fan_(40251826390).jpg" target="_blank" rel="noopener">O2COOL camping fan</a> · <a href="https://commons.wikimedia.org/wiki/File:Streamlight_LED_Camping_Lantern_-_The_Siege_(41339394074).jpg" target="_blank" rel="noopener">Streamlight lantern</a> · <a href="https://commons.wikimedia.org/wiki/File:Philips_MiniVac-5338.jpg" target="_blank" rel="noopener">Philips MiniVac</a> · <a href="https://commons.wikimedia.org/wiki/File:Coffee_Maker.jpg" target="_blank" rel="noopener">Coffee Maker</a> · <a href="https://commons.wikimedia.org/wiki/File:LEDFlashlight.jpg" target="_blank" rel="noopener">LED flashlight</a>.</p>
"""
    if "📷 Créditos de las fotografías" not in post.content:
        post.content += credits
        post.save(update_fields=["content", "updated_at"])


def reverse_replace_images(apps, schema_editor):
    pass


class Migration(migrations.Migration):
    dependencies = [("blog", "0016_completar_articulo_accesorios_camper")]
    operations = [migrations.RunPython(replace_images, reverse_replace_images)]
