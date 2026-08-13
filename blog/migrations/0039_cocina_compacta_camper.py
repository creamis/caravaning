from django.db import migrations
from urllib.parse import quote_plus

POST_SLUG = "que-llevar-cocinar-camper-pequena"
TAG = "caravaning0a-21"
IMAGES = [
    ("https://images.unsplash.com/photo-1544145945-f90425340c7e?auto=format&fit=crop&w=1600&q=85", "Cocina compacta de una camper preparada para cocinar"),
    ("https://images.unsplash.com/photo-1556911220-e15b29be8c8f?auto=format&fit=crop&w=1400&q=85", "Cocina y menaje compacto para una escapada en camper"),
    ("https://images.unsplash.com/photo-1556910103-1c02745aae4d?auto=format&fit=crop&w=1400&q=85", "Utensilios y preparación de comida en una cocina pequeña"),
]

def amazon(query):
    return f"https://www.amazon.es/s?k={quote_plus(query)}&tag={TAG}"

def add_post(apps, schema_editor):
    Post = apps.get_model("blog", "Post")
    PostImage = apps.get_model("blog", "PostImage")
    User = apps.get_model("auth", "User")
    author = User.objects.filter(username="miguel").first() or User.objects.filter(is_superuser=True).order_by("id").first()
    if not author:
        return
    post, _ = Post.objects.get_or_create(
        slug=POST_SLUG,
        defaults={
            "title": "Qué llevar para cocinar en una camper pequeña",
            "author": author,
            "status": "PUBLISHED",
            "content": "",
        },
    )
    post.title = "Qué llevar para cocinar en una camper pequeña"
    post.author = author
    post.status = "PUBLISHED"

    PostImage.objects.filter(post=post).delete()
    for url, _alt in IMAGES:
        PostImage.objects.create(post=post, image_url=url)

    links = {
        "menaje": amazon("menaje camping cocina camper compacto"),
        "sarten": amazon("sarten plegable camping camper"),
        "recipientes": amazon("recipientes plegables silicona camping"),
        "cafetera": amazon("cafetera compacta camping camper"),
        "organizador": amazon("organizador cocina camper autocaravana"),
    }

    post.content = f'''<p>Cocinar en una camper pequeña no significa renunciar a comer bien. La clave está en elegir pocos utensilios, pero que ocupen poco espacio y puedan cumplir varias funciones. En este artículo repasamos qué merece la pena llevar y cómo organizarlo dentro de una cocina de dimensiones reducidas.</p>
<h2>1. Un juego de menaje compacto</h2>
<p>Platos, vasos, cubiertos y utensilios apilables permiten aprovechar mucho mejor los armarios. Para dos personas suele ser suficiente un conjunto reducido que pueda utilizarse a diario.</p>
<p><a href="{links['menaje']}" target="_blank" rel="nofollow sponsored noopener"><strong>🛒 Ver menaje compacto para camping y camper en Amazon</strong></a></p>
<h2>2. Una sartén que ocupe poco</h2>
<p>Una sartén con mango desmontable o plegable resulta especialmente práctica cuando cada centímetro del armario cuenta. Busca un tamaño suficiente para cocinar para dos personas sin convertir la cocina en un tetris culinario.</p>
<p><a href="{links['sarten']}" target="_blank" rel="nofollow sponsored noopener"><strong>🛒 Ver sartenes compactas para camping en Amazon</strong></a></p>
<h2>3. Recipientes plegables y apilables</h2>
<p>Los recipientes de silicona plegable son útiles para guardar comida y, cuando están vacíos, pueden reducir considerablemente el espacio que ocupan.</p>
<p><a href="{links['recipientes']}" target="_blank" rel="nofollow sponsored noopener"><strong>🛒 Ver recipientes plegables para camping en Amazon</strong></a></p>
<h2>4. Una cafetera pequeña</h2>
<p>Si el café forma parte del ritual de viaje, no hace falta llevar una máquina enorme. Una cafetera compacta puede ser suficiente y dejar espacio libre para otros elementos.</p>
<p><a href="{links['cafetera']}" target="_blank" rel="nofollow sponsored noopener"><strong>🛒 Ver cafeteras compactas para camping en Amazon</strong></a></p>
<h2>5. Utensilios multifunción</h2>
<p>Un buen utensilio que sirva para remover, escurrir o servir puede sustituir a varios objetos. Lo mismo ocurre con peladores, abrebotellas y pinzas: antes de comprar varios utensilios, piensa si uno puede resolver varias tareas.</p>
<h2>6. Cómo organizar la cocina de una camper pequeña</h2>
<p>Coloca lo que utilizas todos los días en los lugares más accesibles y reserva las zonas profundas para productos de uso ocasional. Los organizadores pequeños ayudan a evitar que los utensilios se desplacen durante la conducción.</p>
<p><a href="{links['organizador']}" target="_blank" rel="nofollow sponsored noopener"><strong>🛒 Ver organizadores para cocina de camper y autocaravana en Amazon</strong></a></p>
<h2>7. No llenes la cocina por llenar</h2>
<p>En una camper pequeña, cada objeto tiene un coste en espacio. Antes de comprar un accesorio pregúntate cuántas veces lo utilizarás y si puede sustituir a otro utensilio.</p>
<h2>8. Seguridad al cocinar dentro de una camper</h2>
<p>Mantén despejada la zona de cocción, utiliza el combustible y los aparatos siguiendo las instrucciones del fabricante y asegúrate de que existe una ventilación adecuada. Nunca bloquees las rejillas de ventilación del vehículo.</p>
<h2>También te puede interesar</h2>
<p>Si además quieres aprovechar mejor cada centímetro de tu vehículo, consulta nuestra guía sobre <strong>cómo organizar una autocaravana con poco espacio</strong>.</p>
<p><em>Este artículo puede incluir enlaces de afiliado. En calidad de Afiliado de Amazon, obtengo ingresos por las compras adscritas que cumplen los requisitos aplicables, sin coste adicional para ti.</em></p>'''
    post.meta_description = "Qué llevar para cocinar en una camper pequeña: menaje compacto, sartenes plegables, recipientes, cafetera y consejos para organizar la cocina."
    post.save()

class Migration(migrations.Migration):
    dependencies = [("blog", "0038_actualizar_imagenes_invierno_autocaravana")]
    operations = [migrations.RunPython(add_post, migrations.RunPython.noop)]
