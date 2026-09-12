from django.db import migrations
from urllib.parse import quote


AWIN_MID = "105405"
AWIN_AFFID = "2917197"
DESTINATION = "https://www.decathlon.es/es/p/chubasquero-chaqueta-impermeable-hombre-sailing-100-azul/169764/c209c43m8678296"
MARKER = 'data-affiliate="decathlon-sailing100"'


def awin(destination):
    return (
        "https://www.awin1.com/cread.php?"
        f"awinmid={AWIN_MID}&awinaffid={AWIN_AFFID}&ued={quote(destination, safe='')}"
    )


def insert_before_disclosure(content, block):
    lower = content.lower()
    candidates = [
        lower.rfind("enlaces de afiliado"),
        lower.rfind("enlaces afiliados"),
        lower.rfind("afiliado"),
    ]
    disclosure_pos = max(candidates)

    if disclosure_pos == -1:
        return content.rstrip() + "\n\n" + block

    paragraph_pos = lower.rfind("<p", 0, disclosure_pos)
    if paragraph_pos == -1:
        return content[:disclosure_pos] + block + "\n\n" + content[disclosure_pos:]

    return content[:paragraph_pos] + block + "\n\n" + content[paragraph_pos:]


def reinforce_ropa_post(apps, schema_editor):
    Post = apps.get_model("blog", "Post")

    post = Post.objects.filter(
        slug="ropa-imprescindible-caravaning-camping-aire-libre"
    ).first()

    if not post:
        return

    content = post.content or ""
    if MARKER in content:
        return

    deep_link = awin(DESTINATION)

    block = f'''
<section {MARKER}>
  <h2>Una prenda impermeable que sí encaja en una escapada camper</h2>
  <p>Para días de lluvia, viento o paseos desde el camping, una chaqueta ligera impermeable es de esas prendas que ocupan poco y terminan usándose mucho. Una opción concreta es el <strong>Chubasquero impermeable Sailing 100 de Decathlon</strong>, pensado para lluvia moderada, con capucha, tejido cortaviento y tres bolsillos.</p>
  <p><strong>Precio orientativo comprobado: 29,99 €.</strong> El precio puede cambiar, así que conviene revisar el importe actual antes de comprar.</p>
  <p><a href="{deep_link}" target="_blank" rel="nofollow sponsored noopener"><strong>Ver precio actual del Sailing 100 en Decathlon →</strong></a></p>
</section>
'''.strip()

    post.content = insert_before_disclosure(content, block)
    post.save(update_fields=["content"])


class Migration(migrations.Migration):
    dependencies = [
        ("blog", "0064_decathlon_deep_links_images"),
    ]

    operations = [
        migrations.RunPython(reinforce_ropa_post, migrations.RunPython.noop),
    ]
