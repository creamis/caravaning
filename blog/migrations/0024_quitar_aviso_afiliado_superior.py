from django.db import migrations

SLUGS = [
    "tpms-caravana-autocaravana-monitor-presion-neumaticos",
    "como-nivelar-caravana-calzos-rampas-nivel",
    "agua-caravana-depositos-bombas-bidones-accesorios",
    "wc-portatil-camping-camper-caravana-guia-compra",
    "toldo-avance-caravana-guia-compra",
]

NOTICE = "Este artículo puede incluir enlaces de afiliado. En calidad de Afiliado de Amazon, obtengo ingresos por las compras adscritas que cumplen los requisitos aplicables, sin coste adicional para ti."


def remove_top_notice(apps, schema_editor):
    Post = apps.get_model("blog", "Post")
    for post in Post.objects.filter(slug__in=SLUGS):
        content = post.content or ""
        # El aviso no debe aparecer dentro del contenido. La divulgación queda
        # únicamente en el pie del artículo, donde ya se muestra.
        content = content.replace(NOTICE, "")
        content = content.replace(
            f"<p>{NOTICE}</p>",
            "",
        )
        content = content.replace(
            f"<p><em>{NOTICE}</em></p>",
            "",
        )
        post.content = content
        post.save(update_fields=["content", "updated_at"])


def reverse_remove_top_notice(apps, schema_editor):
    pass


class Migration(migrations.Migration):
    dependencies = [("blog", "0023_imagenes_y_enlaces_amazon_guias")]
    operations = [migrations.RunPython(remove_top_notice, reverse_remove_top_notice)]
