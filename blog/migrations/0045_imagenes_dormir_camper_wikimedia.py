from django.db import migrations

POST_SLUG = "accesorios-dormir-mejor-camper"

# URLs estables de Wikimedia Commons. Se usan redirecciones de archivo para
# evitar URLs temporales o hotlinks que dejan de funcionar.
IMAGES = [
    "https://commons.wikimedia.org/wiki/Special:Redirect/file/Bespoke_Volkswagen_campervan_interior_built_by_The_Wee_Camper_Co..jpg",
    "https://commons.wikimedia.org/wiki/Special:Redirect/file/VW_Transporter_Campervan_built_by_The_Wee_Camper_Co..jpg",
    "https://commons.wikimedia.org/wiki/Special:Redirect/file/Campervan_at_the_side_of_the_road_in_the_countryside_with_its_door_open.jpg",
]

ATTRIBUTION = """
<p class="small text-muted"><strong>Créditos de imágenes:</strong> fotografías de interiores y campervan procedentes de Wikimedia Commons, publicadas bajo licencias Creative Commons. Consulta las páginas de archivo para conocer la autoría y condiciones de uso.</p>
"""


def fix_images(apps, schema_editor):
    Post = apps.get_model("blog", "Post")
    PostImage = apps.get_model("blog", "PostImage")

    post = Post.objects.filter(slug=POST_SLUG).first()
    if not post:
        return

    PostImage.objects.filter(post=post).delete()
    for url in IMAGES:
        PostImage.objects.create(post=post, image_url=url)

    if "Créditos de imágenes:" not in post.content:
        post.content += ATTRIBUTION
        post.save(update_fields=["content"])


class Migration(migrations.Migration):
    dependencies = [("blog", "0044_accesorios_dormir_mejor_camper")]
    operations = [migrations.RunPython(fix_images, migrations.RunPython.noop)]
