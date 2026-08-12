from django.db import migrations


POST_SLUG = "lugares-mas-frescos-espana-verano-camper-autocaravana"
OLD_NAVARRA_URL = "https://s0.wklcdn.com/image_37/1128308/172401592/107652111Master.jpg"
NEW_NAVARRA_URL = "https://d2exd72xrrp1s7.cloudfront.net/www/000/1k6/1k/1k934pc0258tr14og6eema3r6d4cx9zxjr-uhi55758763/0?crop=false&q=70&width=1200"
OLD_FLYSCH_URL = "https://img5.juzaphoto.com/001/shared_files/uploads/4683016_m.jpg"
NEW_FLYSCH_URL = "https://www.fotopaises.com/Fotos-Paises/t1024/2015/2/5/2515_1423076063.jpg"


def fix_frescos_verano_images(apps, schema_editor):
    Post = apps.get_model("blog", "Post")
    PostImage = apps.get_model("blog", "PostImage")

    post = Post.objects.filter(slug=POST_SLUG).first()
    if not post:
        return

    # Actualiza las imágenes del carrusel/galería.
    PostImage.objects.filter(post=post, image_url=OLD_NAVARRA_URL).update(image_url=NEW_NAVARRA_URL)
    PostImage.objects.filter(post=post, image_url=OLD_FLYSCH_URL).update(image_url=NEW_FLYSCH_URL)

    # Sustituye las imágenes insertadas dentro del contenido y fuerza una
    # proporción visual uniforme para evitar imágenes excesivamente verticales.
    content = post.content
    content = content.replace(OLD_NAVARRA_URL, NEW_NAVARRA_URL)
    content = content.replace(OLD_FLYSCH_URL, NEW_FLYSCH_URL)

    old_navarra_style = (
        'style="width:100%;height:auto;border-radius:16px;margin:20px 0;">'
    )
    new_navarra_style = (
        'style="width:100%;aspect-ratio:16/9;height:auto;object-fit:cover;'
        'border-radius:16px;margin:20px 0;">'
    )

    navarra_marker = '<img src="' + NEW_NAVARRA_URL + '"'
    navarra_start = content.find(navarra_marker)
    if navarra_start != -1:
        navarra_end = content.find('>', navarra_start)
        if navarra_end != -1:
            tag = content[navarra_start:navarra_end + 1]
            tag = tag.replace(old_navarra_style, new_navarra_style)
            content = content[:navarra_start] + tag + content[navarra_end + 1:]

    flysch_marker = '<img src="' + NEW_FLYSCH_URL + '"'
    flysch_start = content.find(flysch_marker)
    if flysch_start != -1:
        flysch_end = content.find('>', flysch_start)
        if flysch_end != -1:
            tag = content[flysch_start:flysch_end + 1]
            tag = tag.replace(old_navarra_style, new_navarra_style)
            content = content[:flysch_start] + tag + content[flysch_end + 1:]

    post.content = content
    post.save(update_fields=["content", "updated_at"])


def reverse_fix_frescos_verano_images(apps, schema_editor):
    Post = apps.get_model("blog", "Post")
    PostImage = apps.get_model("blog", "PostImage")

    post = Post.objects.filter(slug=POST_SLUG).first()
    if not post:
        return

    PostImage.objects.filter(post=post, image_url=NEW_NAVARRA_URL).update(image_url=OLD_NAVARRA_URL)
    PostImage.objects.filter(post=post, image_url=NEW_FLYSCH_URL).update(image_url=OLD_FLYSCH_URL)

    content = post.content.replace(NEW_NAVARRA_URL, OLD_NAVARRA_URL)
    content = content.replace(NEW_FLYSCH_URL, OLD_FLYSCH_URL)
    post.content = content
    post.save(update_fields=["content", "updated_at"])


class Migration(migrations.Migration):
    dependencies = [
        ("blog", "0012_frescos_verano_imagenes"),
    ]

    operations = [
        migrations.RunPython(fix_frescos_verano_images, reverse_fix_frescos_verano_images),
    ]
