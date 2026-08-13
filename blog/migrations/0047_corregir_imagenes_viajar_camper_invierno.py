from django.db import migrations

POST_SLUG = "viajar-camper-invierno"

IMAGES = [
    "https://res.cloudinary.com/outdoorsy/image/upload/c_limit,w_2880,h_2160/t_odw,a_exif,q_auto,f_webp,h_576,w_768,c_fill/v1643938988/undefined/rentals/278720/images/nwuqnlmxdjwnr6puuat8.jpg",
    "https://www.fenixforinteriors-na.com/en-us/-/media/project/fenix/north-america/article-images/nav-camper/nav-camper-1.webp",
    "https://www.kukucampers.com/media/4/winter-camper-van.jpeg",
]


def update_images(apps, schema_editor):
    Post = apps.get_model("blog", "Post")
    PostImage = apps.get_model("blog", "PostImage")
    post = Post.objects.filter(slug=POST_SLUG).first()
    if not post:
        return
    PostImage.objects.filter(post=post).delete()
    for url in IMAGES:
        PostImage.objects.create(post=post, image_url=url)


class Migration(migrations.Migration):
    dependencies = [("blog", "0046_viajar_camper_invierno")]
    operations = [migrations.RunPython(update_images, migrations.RunPython.noop)]
