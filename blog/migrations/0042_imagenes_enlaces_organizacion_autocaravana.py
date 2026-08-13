from django.db import migrations

POST_SLUG = "organizar-autocaravana-poco-espacio"

IMAGES = [
    ("https://www.outsideonline.com/wp-content/uploads/2023/05/van-life-interior-storage_h.jpg", "Interior de una camper con soluciones de almacenamiento y organización"),
    ("https://www.campervanlife.com/wp-content/uploads/2024/01/campervan-storage-interior.jpg", "Organización del espacio interior de una campervan"),
    ("https://www.thewaywardhome.com/wp-content/uploads/2023/06/van-storage-organization.jpg", "Armarios y almacenamiento organizado dentro de una camper"),
]

AMAZON_LINKS = [
    ("Organizador colgante para camper", "https://www.amazon.es/s?k=organizador+colgante+camper&tag=caravaning0a-21"),
    ("Cajas plegables de almacenamiento", "https://www.amazon.es/s?k=cajas+plegables+almacenamiento+camper&tag=caravaning0a-21"),
    ("Organizador para armario de autocaravana", "https://www.amazon.es/s?k=organizador+armario+autocaravana&tag=caravaning0a-21"),
    ("Bolsas de almacenamiento para camper", "https://www.amazon.es/s?k=bolsas+almacenamiento+camper&tag=caravaning0a-21"),
]


def completar_post(apps, schema_editor):
    Post = apps.get_model("blog", "Post")
    PostImage = apps.get_model("blog", "PostImage")
    post = Post.objects.filter(slug=POST_SLUG).first()
    if not post:
        return

    PostImage.objects.filter(post=post).delete()
    for image_url, _description in IMAGES:
        PostImage.objects.create(post=post, image_url=image_url)

    extra = """
<hr>
<h3>Productos que pueden ayudarte a organizar una autocaravana</h3>
<ul>
<li><a href="https://www.amazon.es/s?k=organizador+colgante+camper&tag=caravaning0a-21" target="_blank" rel="nofollow sponsored noopener">Organizador colgante para camper</a></li>
<li><a href="https://www.amazon.es/s?k=cajas+plegables+almacenamiento+camper&tag=caravaning0a-21" target="_blank" rel="nofollow sponsored noopener">Cajas plegables de almacenamiento</a></li>
<li><a href="https://www.amazon.es/s?k=organizador+armario+autocaravana&tag=caravaning0a-21" target="_blank" rel="nofollow sponsored noopener">Organizador para armario de autocaravana</a></li>
<li><a href="https://www.amazon.es/s?k=bolsas+almacenamiento+camper&tag=caravaning0a-21" target="_blank" rel="nofollow sponsored noopener">Bolsas de almacenamiento para camper</a></li>
</ul>
"""
    if "organizador+colgante+camper" not in post.content:
        post.content = post.content.replace("<hr><p><small>Este artículo puede incluir", extra + "<hr><p><small>Este artículo puede incluir")
        post.save(update_fields=["content"])


class Migration(migrations.Migration):
    dependencies = [("blog", "0041_organizar_autocaravana_poco_espacio")]
    operations = [migrations.RunPython(completar_post, migrations.RunPython.noop)]
