from django.db import migrations


POST_SLUG = "lugares-mas-frescos-espana-verano-camper-autocaravana"

IMAGE_URLS = [
    "https://valledevaldeon.es/wp-content/uploads/2018/07/en-autocaravana-por-el-valle-de-valdeon.jpg",
    "https://www.turismoasturias.es/documents/39908/1373968/lago-enol.jpg/938be681-6a4b-ccc7-60e5-6df88f735f8a?t=1785145333560",
    "https://estaticos-cdn.prensaiberica.es/clip/4669c44c-1a1f-421c-a927-27702128e73f_alta-libre-aspect-ratio_default_0.jpg",
    "https://fotos.hoteles.net/articulos/foz-lugo-10228-3.jpg",
    "https://img5.juzaphoto.com/001/shared_files/uploads/4683016_m.jpg",
    "https://www.nevasport.com/reportajes/img/reportajes/496545/44844.jpg",
    "https://pura-aventura.transforms.svdcdn.com/production/s3/spain-pyrenees-catalonia-aiguestortes-summer-roses-lake--c-diego-pura.jpg?auto=format&dm=1606919630&fit=clip&h=480&q=70&s=e7d2bc918011f7d2cf1428893e657f37",
    "https://s0.wklcdn.com/image_37/1128308/172401592/107652111Master.jpg",
    "https://s1.wklcdn.com/image_82/2473786/31366949/41084710Master.jpg",
    "https://estaticos-cdn.prensaiberica.es/clip/0aa8a87a-fe2b-4241-a19f-6afbf9ef7bdb_alta-libre-aspect-ratio_default_0.jpg",
    "https://cdn2.paraty.es/test4-copia2/images/326f9c7774f1ad1%3Ds800",
]

INLINE_IMAGES = {
    "<h2>1. Asturias y los Picos de Europa</h2>": '<h2>1. Asturias y los Picos de Europa</h2><img src="https://www.turismoasturias.es/documents/39908/1373968/lago-enol.jpg/938be681-6a4b-ccc7-60e5-6df88f735f8a?t=1785145333560" alt="Lagos de Covadonga y Picos de Europa en verano" loading="lazy" style="width:100%;height:auto;border-radius:16px;margin:20px 0;">',
    "<h2>2. Cantabria</h2>": '<h2>2. Cantabria</h2><img src="https://estaticos-cdn.prensaiberica.es/clip/4669c44c-1a1f-421c-a927-27702128e73f_alta-libre-aspect-ratio_default_0.jpg" alt="Costa de Cantabria en verano" loading="lazy" style="width:100%;height:auto;border-radius:16px;margin:20px 0;">',
    "<h2>3. Galicia y la costa de A Mariña Lucense</h2>": '<h2>3. Galicia y la costa de A Mariña Lucense</h2><img src="https://fotos.hoteles.net/articulos/foz-lugo-10228-3.jpg" alt="Playa de Foz en A Mariña Lucense, Galicia" loading="lazy" style="width:100%;height:auto;border-radius:16px;margin:20px 0;">',
    "<h2>4. País Vasco y la costa de Gipuzkoa</h2>": '<h2>4. País Vasco y la costa de Gipuzkoa</h2><img src="https://img5.juzaphoto.com/001/shared_files/uploads/4683016_m.jpg" alt="Flysch de Zumaia en la costa de Gipuzkoa" loading="lazy" style="width:100%;height:auto;border-radius:16px;margin:20px 0;">',
    "<h2>5. Pirineo aragonés</h2>": '<h2>5. Pirineo aragonés</h2><img src="https://www.nevasport.com/reportajes/img/reportajes/496545/44844.jpg" alt="Paisaje del Pirineo aragonés en verano" loading="lazy" style="width:100%;height:auto;border-radius:16px;margin:20px 0;">',
    "<h2>6. Pirineo catalán</h2>": '<h2>6. Pirineo catalán</h2><img src="https://pura-aventura.transforms.svdcdn.com/production/s3/spain-pyrenees-catalonia-aiguestortes-summer-roses-lake--c-diego-pura.jpg?auto=format&dm=1606919630&fit=clip&h=480&q=70&s=e7d2bc918011f7d2cf1428893e657f37" alt="Lago de Aigüestortes en verano" loading="lazy" style="width:100%;height:auto;border-radius:16px;margin:20px 0;">',
    "<h2>7. Navarra y la Selva de Irati</h2>": '<h2>7. Navarra y la Selva de Irati</h2><img src="https://s0.wklcdn.com/image_37/1128308/172401592/107652111Master.jpg" alt="Embalse de Irabia en la Selva de Irati" loading="lazy" style="width:100%;height:auto;border-radius:16px;margin:20px 0;">',
    "<h2>8. Sierra de Gredos</h2>": '<h2>8. Sierra de Gredos</h2><img src="https://s1.wklcdn.com/image_82/2473786/31366949/41084710Master.jpg" alt="Paisaje de montaña en la Sierra de Gredos" loading="lazy" style="width:100%;height:auto;border-radius:16px;margin:20px 0;">',
    "<h2>9. Sierra de Urbión y Laguna Negra</h2>": '<h2>9. Sierra de Urbión y Laguna Negra</h2><img src="https://estaticos-cdn.prensaiberica.es/clip/0aa8a87a-fe2b-4241-a19f-6afbf9ef7bdb_alta-libre-aspect-ratio_default_0.jpg" alt="Laguna Negra de Urbión en Soria" loading="lazy" style="width:100%;height:auto;border-radius:16px;margin:20px 0;">',
    "<h2>10. Valle de Arán</h2>": '<h2>10. Valle de Arán</h2><img src="https://cdn2.paraty.es/test4-copia2/images/326f9c7774f1ad1%3Ds800" alt="Valle de Arán en verano" loading="lazy" style="width:100%;height:auto;border-radius:16px;margin:20px 0;">',
}


def add_images_and_inline_content(apps, schema_editor):
    Post = apps.get_model("blog", "Post")
    PostImage = apps.get_model("blog", "PostImage")

    post = Post.objects.filter(slug=POST_SLUG).first()
    if not post:
        return

    PostImage.objects.filter(post=post).delete()
    for image_url in IMAGE_URLS:
        PostImage.objects.create(post=post, image_url=image_url)

    content = post.content
    for marker, replacement in INLINE_IMAGES.items():
        content = content.replace(marker, replacement, 1)
    post.content = content
    post.save(update_fields=["content", "updated_at"])


def remove_images_and_inline_content(apps, schema_editor):
    Post = apps.get_model("blog", "Post")
    PostImage = apps.get_model("blog", "PostImage")

    post = Post.objects.filter(slug=POST_SLUG).first()
    if not post:
        return

    PostImage.objects.filter(post=post).delete()
    content = post.content
    for replacement in INLINE_IMAGES.values():
        start = replacement.find("<img ")
        if start == -1:
            continue
        image_end = replacement.find(">", start)
        if image_end == -1:
            continue
        image_tag = replacement[start:image_end + 1]
        content = content.replace(image_tag, "", 1)
    post.content = content
    post.save(update_fields=["content", "updated_at"])


class Migration(migrations.Migration):
    dependencies = [
        ("blog", "0011_seed_frescos_verano"),
    ]

    operations = [
        migrations.RunPython(add_images_and_inline_content, remove_images_and_inline_content),
    ]
