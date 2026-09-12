from django.db import migrations

POST_SLUG = "mejores-campings-playa-espana-camper-caravana-autocaravana"

OLD_IMAGE_URL = "https://www.turismocostadorada.com/thumbs/default_desktop/643d5268a15a3_2022-camping-las-palmeras00047-1.jpg"
NEW_IMAGE_URL = "https://static.wixstatic.com/media/259fac_8be4e3ed4f754990a0c797852e11ec2a~mv2.png/v1/fill/w_792%2Ch_432%2Cal_c%2Cq_85%2Cusm_0.66_1.00_0.01%2Cenc_avif%2Cquality_auto/259fac_8be4e3ed4f754990a0c797852e11ec2a~mv2.png"


def replace_cover_image(apps, schema_editor):
    Post = apps.get_model("blog", "Post")
    PostImage = apps.get_model("blog", "PostImage")

    post = Post.objects.filter(slug=POST_SLUG).first()
    if not post:
        return

    old_image = PostImage.objects.filter(post=post, image_url=OLD_IMAGE_URL).first()
    if old_image:
        old_image.image_url = NEW_IMAGE_URL
        old_image.save(update_fields=["image_url"])
    elif not PostImage.objects.filter(post=post, image_url=NEW_IMAGE_URL).exists():
        PostImage.objects.create(post=post, image_url=NEW_IMAGE_URL)


class Migration(migrations.Migration):
    dependencies = [
        ("blog", "0061_imagenes_campings_playa_espana"),
    ]

    operations = [
        migrations.RunPython(replace_cover_image, migrations.RunPython.noop),
    ]
