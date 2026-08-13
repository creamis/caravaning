from django.db import migrations

POST_SLUG = "como-mejorar-iluminacion-camper"
CONTENT = """
<h2>Cómo mejorar la iluminación de una camper</h2>
<p>Una buena iluminación puede cambiar por completo el interior de una camper. No se trata de llenar el vehículo de luces, sino de colocar puntos de luz donde realmente hacen falta y mantener un consumo eléctrico razonable.</p>
<h3>Iluminación principal</h3><p>Una luz LED de techo proporciona iluminación general para cocinar, recoger el interior o preparar la cama. Los modelos LED consumen poco y son una buena opción para instalaciones camper.</p>
<h3>Luz para la zona de cama</h3><p>Una pequeña lámpara de lectura junto a cada plaza permite leer sin iluminar todo el habitáculo.</p>
<h3>Tiras LED</h3><p>Las tiras LED pueden colocarse bajo muebles, en la cocina o alrededor de determinadas zonas del interior para conseguir luz indirecta.</p>
<h3>Luces con sensor</h3><p>Una luz con sensor de movimiento resulta práctica en armarios, escalones y zonas de almacenamiento.</p>
<h3>Iluminación exterior</h3><p>Una luz exterior facilita preparar la cena, sentarse delante de la camper o recoger las bicicletas cuando ya ha oscurecido.</p>
<h3>Controla el consumo</h3><p>Las luces LED tienen un consumo reducido, pero conviene apagarlas cuando no sean necesarias para conservar la batería auxiliar.</p>
<h3>Accesorios útiles</h3>
<ul>
<li><a href="https://www.amazon.es/s?k=lampara+led+techo+camper&tag=caravaning0a-21" target="_blank" rel="nofollow sponsored noopener">Lámpara LED para techo de camper</a></li>
<li><a href="https://www.amazon.es/s?k=tira+led+12v+camper&tag=caravaning0a-21" target="_blank" rel="nofollow sponsored noopener">Tira LED de 12 V</a></li>
<li><a href="https://www.amazon.es/s?k=lampara+lectura+12v+camper&tag=caravaning0a-21" target="_blank" rel="nofollow sponsored noopener">Lámpara de lectura</a></li>
<li><a href="https://www.amazon.es/s?k=luz+sensor+movimiento+12v&tag=caravaning0a-21" target="_blank" rel="nofollow sponsored noopener">Luz con sensor de movimiento</a></li>
</ul>
<p><strong>Consejo:</strong> piensa primero en cómo utilizas cada zona de la camper. Unos pocos puntos de luz bien colocados suelen ser más útiles que una instalación llena de bombillas.</p>
<hr><p><small>Este artículo puede incluir enlaces de afiliado. En calidad de Afiliado de Amazon, obtenemos ingresos por las compras adscritas que cumplen los requisitos aplicables, sin coste adicional para ti.</small></p>
"""

IMAGES = [
    "https://images.unsplash.com/photo-1544634076-8c1f7b5a8c8b?auto=format&fit=crop&w=1200&q=85",
    "https://images.unsplash.com/photo-1510798831971-661eb04b3739?auto=format&fit=crop&w=1200&q=85",
    "https://images.unsplash.com/photo-1500530855697-b586d89ba3ee?auto=format&fit=crop&w=1200&q=85",
]


def create_post(apps, schema_editor):
    Post = apps.get_model("blog", "Post")
    User = apps.get_model("auth", "User")
    PostImage = apps.get_model("blog", "PostImage")
    post = Post.objects.filter(slug=POST_SLUG).first()
    if not post:
        author = User.objects.order_by("id").first()
        if not author:
            return
        post = Post.objects.create(slug=POST_SLUG, title="Cómo mejorar la iluminación de una camper", content=CONTENT, meta_description="Aprende a mejorar la iluminación de una camper con luces LED, tiras LED, lámparas de lectura, sensores y soluciones exteriores.", status="PUBLISHED", author=author)
    else:
        post.content = CONTENT
        post.meta_description = "Aprende a mejorar la iluminación de una camper con luces LED, tiras LED, lámparas de lectura, sensores y soluciones exteriores."
        post.status = "PUBLISHED"
        post.save(update_fields=["content", "meta_description", "status"])
    PostImage.objects.filter(post=post).delete()
    for url in IMAGES:
        PostImage.objects.create(post=post, image_url=url)

class Migration(migrations.Migration):
    dependencies = [("blog", "0050_imagenes_bicicletas_autocaravana_verificadas")]
    operations = [migrations.RunPython(create_post, migrations.RunPython.noop)]
