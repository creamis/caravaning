from django.db import migrations

SLUGS = [
    "mejores-accesorios-para-viajar-en-camper-en-verano",
    "mejor-kit-cocina-camper-accesorios",
    "energia-solar-camper-accesorios-imprescindibles",
    "dormir-fresco-camper-verano",
    "seguridad-camper-accesorios-imprescindibles",
]


def remove_repeated_posts(apps, schema_editor):
    Post = apps.get_model("blog", "Post")
    Post.objects.filter(slug__in=SLUGS).delete()


def restore_repeated_posts(apps, schema_editor):
    # Intentionally empty. These five posts were created by migration 0020
    # and are being removed because they duplicate existing content.
    pass


class Migration(migrations.Migration):
    dependencies = [("blog", "0020_cinco_guias_afiliacion")]
    operations = [migrations.RunPython(remove_repeated_posts, restore_repeated_posts)]
