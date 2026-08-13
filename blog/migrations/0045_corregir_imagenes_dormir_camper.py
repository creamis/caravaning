from django.db import migrations

POST_SLUG = "accesorios-dormir-mejor-camper"

IMAGES = [
    "https://assets.quirkycampers.com/uk/wp-content/uploads/2023/06/Bed-1-scaled.jpg",
    "https://www.challenger-camping-cars.fr/wp-content/uploads/206-premium-lit-seb-1024x683.jpg",
    "https://images.squarespace-cdn.com/content/v1/53358089e4b0a3159186c5a4/1594217904686-TJCO4L6L4SY6NA7ENUIV/_Q1A0216.jpg",
]


def update_images(apps, schema_editor):
    Post = apps.get_model("blog", "Post")
    PostImage = apps.get_model("blog", "PostImage")

    post = Post.objects.filter(slug=POST_SLUG).first()
    if not post:
        return

    PostImage.objects.filter(post=post).delete()
    for image_url in IMAGES:
        PostImage.objects.create(post=post, image_url=image_url)


class Migration(migrations.Migration):
    dependencies = [("blog", "0044_accesorios_dormir_mejor_camper")]
    operations = [migrations.RunPython(update_images, migrations.RunPython.noop)]
