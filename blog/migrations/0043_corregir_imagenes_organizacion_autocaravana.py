from django.db import migrations

POST_SLUG = "organizar-autocaravana-poco-espacio"

# Imágenes reales y directamente relacionadas con organización/almacenamiento
# dentro de campers, caravanas o vehículos de camping.
IMAGES = [
    "https://i.pinimg.com/originals/a2/0a/f1/a20af17ac419a6c7eda5c614697b194d.jpg",
    "https://images.squarespace-cdn.com/content/v1/674c72632e3d592ae6218296/10a3cdfe-c403-4e6a-8037-4dd038aa7c16/Van%2BStorage%2BIdeas",
    "https://vandoit.com/wp-content/uploads/2023/03/40435-25-of-37.jpg",
]


def actualizar_imagenes(apps, schema_editor):
    Post = apps.get_model("blog", "Post")
    PostImage = apps.get_model("blog", "PostImage")

    post = Post.objects.filter(slug=POST_SLUG).first()
    if not post:
        return

    PostImage.objects.filter(post=post).delete()

    for image_url in IMAGES:
        PostImage.objects.create(post=post, image_url=image_url)


class Migration(migrations.Migration):
    dependencies = [
        ("blog", "0042_imagenes_enlaces_organizacion_autocaravana"),
    ]

    operations = [
        migrations.RunPython(actualizar_imagenes, migrations.RunPython.noop),
    ]
