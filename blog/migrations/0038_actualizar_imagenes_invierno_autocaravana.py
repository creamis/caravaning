from django.db import migrations

POST_SLUG = "como-mantener-caliente-autocaravana-invierno"

IMAGES = [
    (
        "https://prcdn.freetls.fastly.net/release_image/129365/5/129365-5-5ade3e2079b31ca02edf207d494caf16-1236x939.jpg?auto=webp&fit=bounds&format=jpeg&height=1260&width=2400",
        "Autocaravana moderna preparada para viajar en invierno sobre nieve",
    ),
    (
        "https://cdn.project-camper.de/wysiwyg/slider/mobile/project-camper-magnet-thermomatten-109-mobile.jpg",
        "Instalación de aislantes térmicos en las ventanas de una camper en invierno",
    ),
    (
        "https://cdn.prod.website-files.com/5ecf709978751abeb9c7ae0b/69aed3d0668f62e80171b9c0_209c9d4d-32a9-4e9d-ae9d-01fc0039c9ec.png",
        "Sistema de calefacción y control de temperatura dentro de una caravana en invierno",
    ),
]


def update_images(apps, schema_editor):
    Post = apps.get_model("blog", "Post")
    PostImage = apps.get_model("blog", "PostImage")

    post = Post.objects.filter(slug=POST_SLUG).first()
    if not post:
        return

    # Sustituimos únicamente las imágenes de este artículo.
    PostImage.objects.filter(post=post).delete()

    for url, alt_text in IMAGES:
        # El modelo PostImage actual no tiene campo alt_text.
        PostImage.objects.create(post=post, image_url=url)


class Migration(migrations.Migration):
    dependencies = [
        ("blog", "0037_como_mantener_caliente_autocaravana_invierno"),
    ]

    operations = [
        migrations.RunPython(update_images, migrations.RunPython.noop),
    ]
