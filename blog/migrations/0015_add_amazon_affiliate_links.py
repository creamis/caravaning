from django.db import migrations
from urllib.parse import quote_plus
import re

POST_SLUG = "20-accesorios-imprescindibles-camper-menos-50-euros"
TAG = "caravaning0a-21"

SEARCHES = [
    ("cargador USB-C", "cargador USB C coche camping"),
    ("power bank", "power bank 20000mah camping"),
    ("lampara LED", "lampara LED camping recargable"),
    ("ventilador portátil", "ventilador camping recargable"),
    ("lámpara antimosquitos", "lampara antimosquitos USB camping"),
    ("mini aspirador", "mini aspirador portatil coche"),
    ("papelera plegable", "papelera plegable camping"),
    ("organizadores", "organizadores camper autocaravana"),
    ("organizador de zapatos", "organizador zapatos camping camper"),
    ("set de cocina", "set cocina camping compacto"),
    ("cafetera portátil", "cafetera portatil camping"),
    ("botellas reutilizables", "botellas reutilizables camping"),
    ("ducha portátil", "ducha portatil camping"),
    ("mesa plegable", "mesa plegable camping"),
    ("ganchos organizadores", "ganchos organizadores camper"),
    ("tendedero portátil", "tendedero portatil camping"),
    ("detector de humo y CO", "detector monoxido carbono humo camping"),
    ("kit de herramientas", "kit herramientas coche camping"),
    ("linterna LED", "linterna LED camping recargable"),
    ("kit de reparación", "kit reparacion camping"),
]


def add_affiliate_links(apps, schema_editor):
    Post = apps.get_model("blog", "Post")
    post = Post.objects.filter(slug=POST_SLUG).first()
    if not post:
        return

    body = post.content
    matches = list(re.finditer(r'(<img[^>]*alt="[^"]*"[^>]*>)', body))

    for index, (label, query) in enumerate(SEARCHES):
        if index >= len(matches):
            break
        url = f"https://www.amazon.es/s?k={quote_plus(query)}&tag={TAG}"
        marker = f"<!-- amazon-affiliate:{index} -->"
        if marker in body:
            continue
        current_matches = list(re.finditer(r'(<img[^>]*alt="[^"]*"[^>]*>)', body))
        if index >= len(current_matches):
            continue
        end = current_matches[index].end()
        cta = (
            f' {marker}<p style="margin:12px 0 24px;">'
            f'<a href="{url}" target="_blank" rel="nofollow sponsored noopener" '
            f'style="display:inline-block;padding:12px 18px;border-radius:10px;'
            f'background:#ff9900;color:#111;text-decoration:none;font-weight:700;">'
            f'🛒 Ver {label} en Amazon</a></p>'
        )
        body = body[:end] + cta + body[end:]

    disclosure = (
        '<div style="margin:28px 0;padding:16px;border:1px solid #ddd;border-radius:12px;">'
        '<strong>Nota de afiliación:</strong> Algunos enlaces de este artículo son enlaces de afiliado. '
        'Si realizas una compra después de acceder a ellos, Caravaning Project puede recibir una comisión '
        'sin que esto suponga un coste adicional para ti. Los precios y la disponibilidad pueden cambiar.'
        '</div>'
    )
    if "Nota de afiliación:" not in body:
        body = disclosure + body

    post.content = body
    post.save(update_fields=["content"])


def remove_affiliate_links(apps, schema_editor):
    Post = apps.get_model("blog", "Post")
    post = Post.objects.filter(slug=POST_SLUG).first()
    if not post:
        return
    body = re.sub(r'\s*<!-- amazon-affiliate:\d+ -->.*?</p>', '', post.content, flags=re.DOTALL)
    body = re.sub(r'<div style="margin:28px 0;padding:16px;border:1px solid #ddd;border-radius:12px;">.*?</div>', '', body, flags=re.DOTALL)
    post.content = body
    post.save(update_fields=["content"])


class Migration(migrations.Migration):
    dependencies = [("blog", "0014_accesorios_camper_imagenes")]
    operations = [migrations.RunPython(add_affiliate_links, remove_affiliate_links)]
