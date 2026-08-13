from django.db import migrations

POST_SLUG = "que-llevar-cocinar-camper-pequena"

IMAGES = [
    ("https://" + "www.thewaywardhome.com" + "/wp-content/uploads/2022/02/Revel-Interior-1.jpg", "Cocina compacta de una camper moderna preparada para cocinar"),
    ("https://" + "nativecampervans.com" + "/app/uploads/2023/03/Native-Campervans_USA_Bastiani-73-min.jpg", "Cocina exterior de una campervan durante una escapada de camping"),
    ("https://" + "kombilife.com.au" + "/cdn/shop/files/vanessa-heckauszug-ford-tourneo-custom-mit-frischwasser-zulauf_600x400.jpg?v=1714181071", "Cocina compacta instalada en la parte trasera de una campervan"),
]


def actualizar_imagenes(apps, schema_editor):
    Post = apps.get_model("blog", "Post")
    PostImage = apps.get_model("blog", "PostImage")
    post = Post.objects.filter(slug=POST_SLUG).first()
    if not post:
        return
    PostImage.objects.filter(post=post).delete()
    for image_url, _description in IMAGES:
        PostImage.objects.create(post=post, image_url=image_url)


class Migration(migrations.Migration):
    dependencies = [("blog", "0039_cocina_compacta_camper")]
    operations = [migrations.RunPython(actualizar_imagenes, migrations.RunPython.noop)]
