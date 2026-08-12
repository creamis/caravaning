from django.db import migrations

POST_SLUG = "20-accesorios-imprescindibles-camper-menos-50-euros"

# Fotografías de producto/categoría más limpias y actuales, una por accesorio.
# Se mantienen los enlaces de Amazon y solo se sustituyen las imágenes.
IMAGE_URLS = [
    "https://media2.gsm55.com/media/catalog/product/images/c/cac-sws-1907/neutre/cac-sws-1907-1.jpg",
    "https://i.ebayimg.com/images/g/rNYAAeSwZ59pRyI8/s-l1200.png",
    "https://m.media-amazon.com/images/I/61MN06k5w%2BL.jpg",
    "https://www.bigw.com.au/medias/sys_master/images/images/hdf/h3c/122558983241758.jpg",
    "https://cdn11.bigcommerce.com/s-0esxpuxvq8/images/stencil/1280x1280/products/94274/363235/lumi-mosi-killer-lantern-2__72860.1720427237.jpg?c=1",
    "https://i5.walmartimages.com/asr/b88a87a6-04a9-4c7c-982f-be034c76d037.2a2e1fe88c7f55bf39ef158172ef33d6.jpeg?odnBg=FFFFFF&odnHeight=612&odnWidth=612",
    "https://mpcamp.pl/environment/cache/images/productGfx_73033_750_750/Kosz-na-smieci-5-l---Camp4.webp",
    "https://www.bfgcdn.com/600_600_90/580-1236/outwell-margate-kitchen-storage-box-campingkasten-detail-4.jpg",
    "https://www.muchocamping.com/cdnassets/organizador-zapatos-plegable-avance-caravana_l.jpg",
    "https://i5.walmartimages.com/seo/Camping-Cookware-Set-Camping-Equipment-Campfire-Utensils-Non-stick-Cooking-Equipment-Lightweight-Stackable-Pots-Bowls-Storage-Bag-Suitable-Outdoor-Hi_04029087-bb63-4a12-8911-27a7b7af7b84.b3f24e606546a4839e041b502136042c.jpeg",
    "https://upload.jaknot.com/2026/02/images/products/b71994/original/one-two-cups-portable-coffee-maker-2in1-nespresso-20-bar-1800mah-hs9440-1s.jpg",
    "https://magourde.com/cdn/shop/files/gourdegrossecapaciteeninoxverte.jpg?v=1722120509&width=1458",
    "https://naturenomad.fr/cdn/shop/files/Sfb7ebbef45bb4fb28e8ea84407098906e_1.webp?v=1752929410",
    "https://3pmedia.leroymerlin.co.za/SOURCE/4f23fd536c4a47628d25c606066a7181",
    "https://himall-storage-1259069382.cos.ap-nanjing.myqcloud.com/web/Storage/Shop/1543/Products/42291/1.png",
    "https://media.s-bol.com/RG8LKRXGAqmq/k57oKGE/550x503.jpg",
    "https://cdn.vergleich.org/v2/comparison-tables/aegislink-sc200.jpg?d=1000x1000&fill=true&q=70",
    "https://www.sunsetandco.com/cdn/shop/files/FixItKit_Black.1.webp?v=1717540062&width=1080",
    "https://m.media-amazon.com/images/I/61h06bJBP2L.jpg",
    "https://storage.ghost.io/c/9a/93/9a93dd78-e82f-4615-a68d-0688ab73e1c9/content/images/2024/07/711R4J3vW8L._AC_SL1500_.jpg",
]


def replace_images(apps, schema_editor):
    Post = apps.get_model("blog", "Post")
    PostImage = apps.get_model("blog", "PostImage")

    post = Post.objects.filter(slug=POST_SLUG).first()
    if not post:
        return

    content = post.content
    cursor = 0
    for new_url in IMAGE_URLS:
        img_start = content.find('<img src="', cursor)
        if img_start == -1:
            break
        url_start = img_start + len('<img src="')
        url_end = content.find('"', url_start)
        if url_end == -1:
            break
        content = content[:url_start] + new_url + content[url_end:]
        cursor = url_start + len(new_url)

    post.content = content
    post.save(update_fields=["content", "updated_at"])

    # Sincroniza la galería/cabecera para que no conserve las imágenes antiguas.
    # La primera imagen de PostImage seguirá siendo la portada del artículo.
    PostImage.objects.filter(post=post).delete()
    cover = "https://images.unsplash.com/photo-1523987355523-c7b5b0dd90a7?auto=format&fit=crop&w=1600&q=85"
    PostImage.objects.create(post=post, image_url=cover)
    for url in IMAGE_URLS:
        PostImage.objects.get_or_create(post=post, image_url=url)


def reverse_replace_images(apps, schema_editor):
    pass


class Migration(migrations.Migration):
    dependencies = [("blog", "0027_corregir_imagen_agua_caravana")]
    operations = [migrations.RunPython(replace_images, reverse_replace_images)]
