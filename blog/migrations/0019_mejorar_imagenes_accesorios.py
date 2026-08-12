import re
from django.db import migrations

POST_SLUG = "20-accesorios-imprescindibles-camper-menos-50-euros"

CORRECTED = {
    7: "https://commons.wikimedia.org/wiki/Special:Redirect/file/Trash_can.jpg",
    8: "https://commons.wikimedia.org/wiki/Special:Redirect/file/Blue_plastic_storage_organizer_boxes_for_screws.jpg",
    9: "https://commons.wikimedia.org/wiki/Special:Redirect/file/Shoe_Rack.jpg",
    12: "https://commons.wikimedia.org/wiki/Special:Redirect/file/Owala_Water_Bottle.jpg",
    13: "https://commons.wikimedia.org/wiki/Special:Redirect/file/Camping_showers_(4613626640).jpg",
    14: "https://commons.wikimedia.org/wiki/Special:Redirect/file/Geometric-design-on-a-folding-camping-table.png",
    15: "https://commons.wikimedia.org/wiki/Special:Redirect/file/Coat_hook_C.jpg",
    16: "https://commons.wikimedia.org/wiki/Special:Redirect/file/Clothesline_(9459404442).jpg",
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


def improve_images(apps, schema_editor):
    Post = apps.get_model("blog", "Post")
    PostImage = apps.get_model("blog", "PostImage")
    post = Post.objects.filter(slug=POST_SLUG).first()
    if not post:
        return

    for number, url in CORRECTED.items():
        post.content = replace_nth_image(post.content, number, url)
    post.save(update_fields=["content", "updated_at"])

    PostImage.objects.filter(post=post).delete()
    cover = "https://commons.wikimedia.org/wiki/Special:Redirect/file/Volkswagen-Combi-T2-Adventure-Awaits-byRundvald.jpg"
    PostImage.objects.create(post=post, image_url=cover)
    urls = re.findall(r'<img\s+[^>]*?src=[\"\'](.*?)[\"\']', post.content, flags=re.IGNORECASE)
    for url in urls[:20]:
        PostImage.objects.get_or_create(post=post, image_url=url)

    marker = "<h3>📷 Última selección de fotografías</h3>"
    if marker not in post.content:
        post.content += """
<hr>
<h3>📷 Última selección de fotografías</h3>
<p>Hemos vuelto a revisar estos apartados para que cada imagen tenga una relación visual clara con el accesorio descrito. Las fotografías proceden de Wikimedia Commons y se utilizan como referencia visual del tipo de producto; no implican que el objeto fotografiado sea exactamente el producto enlazado en Amazon.</p>
<p><a href="https://commons.wikimedia.org/wiki/File:Trash_can.jpg" target="_blank" rel="noopener">Papelera</a> · <a href="https://commons.wikimedia.org/wiki/File:Blue_plastic_storage_organizer_boxes_for_screws.jpg" target="_blank" rel="noopener">Organizadores</a> · <a href="https://commons.wikimedia.org/wiki/File:Shoe_Rack.jpg" target="_blank" rel="noopener">Zapatero</a> · <a href="https://commons.wikimedia.org/wiki/File:Owala_Water_Bottle.jpg" target="_blank" rel="noopener">Botella reutilizable</a> · <a href="https://commons.wikimedia.org/wiki/File:Camping_showers_(4613626640).jpg" target="_blank" rel="noopener">Ducha de camping</a> · <a href="https://commons.wikimedia.org/wiki/File:Geometric-design-on-a-folding-camping-table.png" target="_blank" rel="noopener">Mesa plegable de camping</a> · <a href="https://commons.wikimedia.org/wiki/File:Coat_hook_C.jpg" target="_blank" rel="noopener">Gancho</a> · <a href="https://commons.wikimedia.org/wiki/File:Clothesline_(9459404442).jpg" target="_blank" rel="noopener">Tendedero</a>.</p>
"""
        post.save(update_fields=["content", "updated_at"])


def reverse_improve_images(apps, schema_editor):
    pass


class Migration(migrations.Migration):
    dependencies = [("blog", "0018_corregir_imagenes_accesorios")]
    operations = [migrations.RunPython(improve_images, reverse_improve_images)]
