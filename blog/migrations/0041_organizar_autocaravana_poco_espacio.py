from django.db import migrations

SLUG = "organizar-autocaravana-poco-espacio"


def create_post(apps, schema_editor):
    Post = apps.get_model("blog", "Post")
    User = apps.get_model("auth", "User")
    author = User.objects.order_by("id").first()
    if not author:
        return

    post, created = Post.objects.get_or_create(
        slug=SLUG,
        defaults={
            "title": "Cómo organizar una autocaravana con poco espacio",
            "content": """<h2>Cómo organizar una autocaravana con poco espacio</h2>
<p>En una camper o autocaravana cada centímetro cuenta. Una buena organización permite viajar con lo necesario sin llenar el habitáculo de objetos y facilita encontrar todo cuando estamos de ruta.</p>
<h3>1. Aprovecha los espacios verticales</h3><p>Puertas, paredes y laterales de armarios pueden convertirse en zonas de almacenamiento. Los organizadores colgantes y pequeños ganchos permiten guardar objetos de uso frecuente sin ocupar las zonas de paso.</p>
<h3>2. Ordena los armarios por categorías</h3><p>Reserva zonas concretas para cocina, ropa, higiene y herramientas. Los recipientes apilables ayudan a aprovechar la altura y evitan que los objetos se desplacen durante el viaje.</p>
<h3>3. Aprovecha el espacio bajo la cama</h3><p>El arcón bajo la cama suele ser uno de los mayores espacios de almacenamiento. Utiliza bolsas o cajas de diferentes tamaños para mantenerlo dividido y deja más accesibles las cosas que utilizas durante la ruta.</p>
<h3>4. Una cocina pequeña necesita soluciones compactas</h3><p>En una cocina camper funcionan especialmente bien los utensilios plegables, recipientes que encajan unos dentro de otros y productos multifunción. Así puedes cocinar sin dedicar un armario entero al menaje.</p>
<h3>5. No olvides las zonas de acceso</h3><p>Los bolsillos organizadores y pequeños sistemas de almacenamiento junto a la entrada pueden servir para llaves, cables, linternas y otros objetos que conviene tener a mano.</p>
<h3>6. Menos objetos significa más comodidad</h3><p>Antes de guardar algo, piensa si realmente lo utilizarás durante el viaje. En una autocaravana pequeña, reducir objetos innecesarios suele aportar más espacio que comprar más sistemas de almacenamiento.</p>
<h3>Productos que pueden ayudarte</h3><p>Para completar la organización puedes utilizar organizadores plegables, bolsas de almacenamiento, cajas apilables y accesorios para aprovechar puertas y armarios. Antes de comprar, comprueba siempre las medidas disponibles en tu vehículo.</p>
<p>También puedes consultar nuestra guía sobre <a href="/blog/que-llevar-para-cocinar-en-una-camper-pequena/">qué llevar para cocinar en una camper pequeña</a> y nuestra guía sobre <a href="/blog/como-mantener-caliente-autocaravana-invierno/">cómo mantener caliente una autocaravana en invierno</a>.</p>
<p><strong>Consejo final:</strong> organiza el vehículo pensando en cómo te mueves dentro de él. Lo que utilizas cada día debe quedar accesible y lo que utilizas ocasionalmente puede ocupar los espacios menos cómodos.</p>
<hr><p><small>Este artículo puede incluir enlaces de afiliado. En calidad de Afiliado de Amazon, obtengo ingresos por las compras adscritas que cumplen los requisitos aplicables, sin coste adicional para ti.</small></p>""",
            "author": author,
            "status": "PUBLISHED",
        },
    )
    if not created:
        post.status = "PUBLISHED"
        post.save(update_fields=["status"])


def reverse(apps, schema_editor):
    apps.get_model("blog", "Post").objects.filter(slug=SLUG).delete()


class Migration(migrations.Migration):
    dependencies = [("blog", "0040_actualizar_imagenes_cocina_camper")]
    operations = [migrations.RunPython(create_post, reverse)]
