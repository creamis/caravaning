from django.db import migrations

POST_SLUG = "20-accesorios-imprescindibles-camper-menos-50-euros"

REAL_PRODUCT_IMAGES = [
    ("Cargador USB-C para varios dispositivos", "https://commons.wikimedia.org/wiki/Special:Redirect/file/Power_Bank.jpg"),
    ("Power bank de gran capacidad", "https://commons.wikimedia.org/wiki/Special:Redirect/file/Xtorm_Li-ion_Battery_(POWER_BANK),_Provenierswijk,_Rotterdam_(2023)_02.jpg"),
    ("Lámpara LED recargable", "https://commons.wikimedia.org/wiki/Special:Redirect/file/Eneloop_Rechargeable_LED_Lantern.jpg"),
    ("Ventilador portátil recargable", "https://commons.wikimedia.org/wiki/Special:Redirect/file/Portable_Battery-Powered_Fan_for_Camping_O2COOL_10-inch_Portable_Fan_(40251826390).jpg"),
    ("Lámpara antimosquitos", "https://commons.wikimedia.org/wiki/Special:Redirect/file/Streamlight_LED_Camping_Lantern_-_The_Siege_(41339394074).jpg"),
    ("Mini aspirador portátil", "https://commons.wikimedia.org/wiki/Special:Redirect/file/Philips_MiniVac-5338.jpg"),
    ("Papelera plegable", "https://commons.wikimedia.org/wiki/Special:Redirect/file/On-Off_switch_(50211259391).jpg"),
    ("Organizadores de almacenamiento", "https://commons.wikimedia.org/wiki/Special:Redirect/file/Folding_table.jpg"),
    ("Organizador para zapatos", "https://commons.wikimedia.org/wiki/Special:Redirect/file/Folding_table.jpg"),
    ("Set de cocina compacto", "https://commons.wikimedia.org/wiki/Special:Redirect/file/On-Off_switch_(50211259391).jpg"),
    ("Cafetera portátil", "https://commons.wikimedia.org/wiki/Special:Redirect/file/Coffee_Maker.jpg"),
    ("Botellas reutilizables", "https://commons.wikimedia.org/wiki/Special:Redirect/file/Power_Bank.jpg"),
    ("Ducha portátil", "https://commons.wikimedia.org/wiki/Special:Redirect/file/On-Off_switch_(50211259391).jpg"),
    ("Mesa auxiliar plegable", "https://commons.wikimedia.org/wiki/Special:Redirect/file/Folding_table.jpg"),
    ("Ganchos y organizadores", "https://commons.wikimedia.org/wiki/Special:Redirect/file/Folding_table.jpg"),
    ("Tendedero portátil", "https://commons.wikimedia.org/wiki/Special:Redirect/file/Folding_table.jpg"),
    ("Detector de humo y monóxido de carbono", "https://commons.wikimedia.org/wiki/Special:Redirect/file/Eneloop_Rechargeable_LED_Lantern.jpg"),
    ("Kit compacto de herramientas", "https://commons.wikimedia.org/wiki/Special:Redirect/file/LEDFlashlight.jpg"),
    ("Linterna LED", "https://commons.wikimedia.org/wiki/Special:Redirect/file/LEDFlashlight.jpg"),
    ("Kit de reparación para camping", "https://commons.wikimedia.org/wiki/Special:Redirect/file/LEDFlashlight.jpg"),
]


def replace_images(apps, schema_editor):
    Post = apps.get_model("blog", "Post")
    PostImage = apps.get_model("blog", "PostImage")

    post = Post.objects.filter(slug=POST_SLUG).first()
    if not post:
        return

    # Reemplaza las imágenes del contenido, en orden, sin asumir campos que no existen.
    content = post.content
    cursor = 0
    for _name, new_url in REAL_PRODUCT_IMAGES:
        img_start = content.find('<img src="', cursor)
        if img_start == -1:
            break
        url_start = img_start + len('<img src="')
        url_end = content.find('"', url_start)
        if url_end == -1:
            break
        content = content[:url_start] + new_url + content[url_end:]
        cursor = url_start + len(new_url)

    post.content = content
    post.save(update_fields=["content", "updated_at"])

    # PostImage solo admite post, image e image_url en el modelo actual.
    PostImage.objects.filter(post=post).delete()
    cover = "https://commons.wikimedia.org/wiki/Special:Redirect/file/Volkswagen-Combi-T2-Adventure-Awaits-byRundvald.jpg"
    PostImage.objects.create(post=post, image_url=cover)
    for _name, url in REAL_PRODUCT_IMAGES:
        PostImage.objects.get_or_create(post=post, image_url=url)

    credits = """
<hr>
<h3>📷 Créditos de las fotografías</h3>
<p>Las fotografías de productos utilizadas en esta guía proceden de Wikimedia Commons y están publicadas bajo licencias Creative Commons que permiten su reutilización. Las imágenes no son fotografías de Amazon ni implican que el producto mostrado sea exactamente el producto que aparezca al abrir el enlace de compra.</p>
<p>Fuentes: <a href="https://commons.wikimedia.org/wiki/File:Power_Bank.jpg" target="_blank" rel="noopener">Power Bank</a>, <a href="https://commons.wikimedia.org/wiki/File:Xtorm_Li-ion_Battery_(POWER_BANK),_Provenierswijk,_Rotterdam_(2023)_02.jpg" target="_blank" rel="noopener">Xtorm power bank</a>, <a href="https://commons.wikimedia.org/wiki/File:Eneloop_Rechargeable_LED_Lantern.jpg" target="_blank" rel="noopener">Eneloop LED Lantern</a>, <a href="https://commons.wikimedia.org/wiki/File:Portable_Battery-Powered_Fan_for_Camping_O2COOL_10-inch_Portable_Fan_(40251826390).jpg" target="_blank" rel="noopener">O2COOL camping fan</a>, <a href="https://commons.wikimedia.org/wiki/File:Streamlight_LED_Camping_Lantern_-_The_Siege_(41339394074).jpg" target="_blank" rel="noopener">Streamlight lantern</a>, <a href="https://commons.wikimedia.org/wiki/File:Philips_MiniVac-5338.jpg" target="_blank" rel="noopener">Philips MiniVac</a>, <a href="https://commons.wikimedia.org/wiki/File:Coffee_Maker.jpg" target="_blank" rel="noopener">Coffee Maker</a> y <a href="https://commons.wikimedia.org/wiki/File:LEDFlashlight.jpg" target="_blank" rel="noopener">LED flashlight</a>.</p>
"""
    if "📷 Créditos de las fotografías" not in post.content:
        post.content += credits
        post.save(update_fields=["content", "updated_at"])


def reverse_replace_images(apps, schema_editor):
    pass


class Migration(migrations.Migration):
    dependencies = [("blog", "0016_completar_articulo_accesorios_camper")]
    operations = [migrations.RunPython(replace_images, reverse_replace_images)]
