from django.db import migrations

SLUG = "caravaning-no-es-solo-para-el-verano"
COVER = "https://cdn.prod.v2.camping.info/media/campsites/camping-le-palme/ZBUO2P-A22S3.jpg"

IMAGES = {
    "winter": "https://cdn.freeontour.com/photos_v2/c630ed1fb8d40d0deacd59447fe4dffbfe6b1f28442de1230875608c81d71c4c/xlarge.jpg?format=auto",
    "autumn": "https://www.campcruisers.com/landingpage/campervan/wohnmobil_mieten_slovakia_why-you-should-book-your-campervan-for-slovakia-online-2.png",
    "spring": "https://cdn.prod.website-files.com/609171e52ab58f79692ae11b/699c3390d5d28d72c548d2a0_alpes-francaises-road-trip-printemps.jpg",
}


def update_post(apps, schema_editor):
    Post = apps.get_model("blog", "Post")
    PostImage = apps.get_model("blog", "PostImage")
    post = Post.objects.filter(slug=SLUG).first()
    if not post:
        return

    content = post.content
    replacements = {
        'https://images.unsplash.com/photo-1510798831971-661eb04b3739?auto=format&fit=crop&w=1400&q=85': IMAGES["winter"],
        'https://images.unsplash.com/photo-1500534623283-312aade485b7?auto=format&fit=crop&w=1400&q=85': IMAGES["autumn"],
        'https://images.unsplash.com/photo-1501785888041-af3ef285b470?auto=format&fit=crop&w=1400&q=85': IMAGES["spring"],
    }
    for old, new in replacements.items():
        content = content.replace(old, new)

    content = content.replace(
        'alt="Paisaje invernal para viajar en autocaravana"',
        'alt="Autocaravana preparada para viajar en invierno entre nieve y montañas"'
    )
    content = content.replace(
        'alt="Paisaje otoñal para una escapada en camper"',
        'alt="Camper viajando por una carretera entre bosques de otoño"'
    )
    content = content.replace(
        'alt="Paisaje natural para viajar en camper en primavera"',
        'alt="Camper junto a un paisaje alpino en primavera"'
    )

    post.content = content
    post.save(update_fields=["content"])

    PostImage.objects.filter(post=post).delete()
    PostImage.objects.create(post=post, image_url=COVER)


def reverse_update(apps, schema_editor):
    pass


class Migration(migrations.Migration):
    dependencies = [("blog", "0029_post_caravaning_todo_el_ano")]
    operations = [migrations.RunPython(update_post, reverse_update)]
