from django.db import migrations
from urllib.parse import quote

AWIN_MID = "105405"
AWIN_AFFID = "2917197"

PRODUCTS = [
    {
        "keywords": ["BL100", "Lampara de camping recargable Quechua BL100", "Lámpara de camping recargable Quechua BL100"],
        "destination": "https://www.decathlon.es/es/p/lampara-de-camping-100-lumenes-ipx4-pilas-incluidas-quechua-bl100/172514/c98c66m8492468",
        "image_url": None,
    },
    {
        "keywords": ["Ice Compact 30", "Mochila nevera Quechua Ice Compact 30 L", "Mochila nevera 30L Quechua Ice Compact"],
        "destination": "https://www.decathlon.es/es/p/mochila-nevera-30l-quechua-ice-compact/309970/c328m8913720",
        "image_url": "https://contents.mediadecathlon.com/p2837133/k%243a81aef5237cc599943bb1a70022209a/picture.jpg?f=3000x0&format=auto",
    },
    {
        "keywords": ["Mueble de cocina camping Quechua", "Mueble de cocina de camping L"],
        "destination": "https://www.decathlon.es/es/p/mueble-de-cocina-de-camping-l-plegable-y-con-mampara/354898/m8882499",
        "image_url": "https://contents.mediadecathlon.com/p2999833/k%2488269d9c4fc2ffc56496674dd0812124/picture.jpg?f=3000x0&format=auto",
    },
    {
        "keywords": ["Silla plegable camping Quechua con reposabrazos", "Silla plegable de camping con reposabrazos Quechua Basic"],
        "destination": "https://www.decathlon.es/es/p/silla-plegable-de-camping-con-reposabrazos-quechua-basic/13372/c98m8852991",
        "image_url": "https://contents.mediadecathlon.com/p2598175/k%24ef0cd18cf948c705e900c9cf2e92dc64/picture.jpg?f=3000x0&format=auto",
    },
    {
        "keywords": ["Mesa plegable camping 4 personas Quechua", "Mesa plegable de camping, 4 personas"],
        "destination": "https://www.decathlon.es/es/p/mesa-plegable-de-camping-4-personas-marron/303341/c14m8950609",
        "image_url": "https://contents.mediadecathlon.com/p3088743/k%2475e2fa1fcc604d69ff3503ce69de2cec/picture.jpg?f=3000x0&format=auto",
    },
]


def awin(destination):
    return (
        "https://www.awin1.com/cread.php?"
        f"awinmid={AWIN_MID}&awinaffid={AWIN_AFFID}&ued={quote(destination, safe='')}"
    )


def update_posts(apps, schema_editor):
    Post = apps.get_model("blog", "Post")
    PostImage = apps.get_model("blog", "PostImage")

    for post in Post.objects.all():
        content = post.content or ""
        original = content

        for item in PRODUCTS:
            deep_link = awin(item["destination"])
            matched = item["destination"] in content or any(keyword.lower() in content.lower() for keyword in item["keywords"])
            if not matched:
                continue

            content = content.replace(item["destination"], deep_link)

            # Replace common non-affiliate Decathlon links to the same product, including tracking suffixes.
            base_destination = item["destination"].split("?")[0]
            content = content.replace(base_destination, deep_link)

            # If the product is mentioned but there is no CTA yet, add one at the end of the article.
            if deep_link not in content:
                label = item["keywords"][0]
                content += (
                    f'<p><a href="{deep_link}" target="_blank" '
                    'rel="nofollow sponsored noopener"><strong>'
                    f'Ver {label} en Decathlon →</strong></a></p>'
                )

            if item["image_url"]:
                PostImage.objects.get_or_create(
                    post=post,
                    image_url=item["image_url"],
                )

        if content != original:
            post.content = content
            post.save(update_fields=["content"])


class Migration(migrations.Migration):
    dependencies = [
        ("blog", "0063_mejorar_guia_instalacion_solar_autocaravanas"),
    ]

    operations = [
        migrations.RunPython(update_posts, migrations.RunPython.noop),
    ]
