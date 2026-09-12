from django.db import migrations


POST_SLUG = "campings-ninos-espana-vacaciones-familia"

# Imágenes verificadas de campings incluidos en el artículo.
# La primera se usa como portada y no coincide con las portadas empleadas
# en los artículos anteriores de campings.
IMAGES = [
    "https://cdn2.paraty.es/creixell/images/efa9dc8b862df11",
    "https://static5.maeva.com/ws-photos/FRANCE/vilanova-i-la-geltru/residences/camping-vilanova-park/12a91baf0095bf49f7d8664a2cf6923c.jpg?crop=1&ext=jpg&h=480&w=800",
    "https://res.cloudinary.com/eurocamp/image/upload/t_900x508/f_auto/CD018-miami-platja-la-torre-del-sol-pools-costa-dorada-pirate-pool-e_tcm13-47092.jpg",
    "https://www.campings.com/img/_/partner-large/76974/d083f742-0b61-4137-8d6a-6362ec70e66b.jpg/b2b-partner-11.jpg",
    "https://www.campingscomunidadvalenciana.es/wp-content/uploads/2020/12/CAMPING-MARJAL-GUARDAMAR_GUARDAMAR-DE-SEGURA_ALICANTE_01.jpg",
    "https://static.wixstatic.com/media/4da582_72a0686621bd440cb7149600d464955d~mv2.jpg/v1/fill/w_670%2Ch_447%2Cal_c%2Cq_80%2Cenc_avif%2Cquality_auto/4da582_72a0686621bd440cb7149600d464955d~mv2.jpg",
]


def add_images(apps, schema_editor):
    Post = apps.get_model("blog", "Post")
    PostImage = apps.get_model("blog", "PostImage")

    post = Post.objects.filter(slug=POST_SLUG).first()
    if not post:
        post = Post.objects.filter(title__icontains="Campings para ir con niños en España").first()
    if not post:
        return

    # Este post nació sin imágenes en 0072. Limpiamos únicamente sus imágenes
    # para que el orden de la galería sea determinista y la portada sea la primera.
    PostImage.objects.filter(post=post).delete()

    for url in IMAGES:
        PostImage.objects.create(post=post, image_url=url)


class Migration(migrations.Migration):
    dependencies = [
        ("blog", "0072_campings_ninos_espana_camping_and_co"),
    ]

    operations = [
        migrations.RunPython(add_images, migrations.RunPython.noop),
    ]
