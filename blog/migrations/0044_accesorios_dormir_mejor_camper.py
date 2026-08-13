from django.db import migrations

POST_SLUG = "accesorios-dormir-mejor-camper"

IMAGES = [
    ("https://images.unsplash.com/photo-1544620347-c4fd4a3d5957?auto=format&fit=crop&w=1600&q=85", "Camper preparada para dormir durante un viaje"),
    ("https://images.unsplash.com/photo-1504851149312-7a075b496cc7?auto=format&fit=crop&w=1600&q=85", "Zona de descanso en un entorno de camping"),
    ("https://images.unsplash.com/photo-1510798831971-661eb04b3739?auto=format&fit=crop&w=1600&q=85", "Camper y zona de acampada para descansar"),
]

CONTENT = """
<h2>Accesorios para dormir mejor en una camper</h2>
<p>Dormir en una camper puede ser una de las mejores partes del viaje, pero una cama incómoda, demasiada luz o falta de ventilación pueden convertir la noche en una pequeña batalla. Con algunos accesorios bien elegidos puedes ganar comodidad sin llenar de trastos el vehículo.</p>
<h3>1. Un buen topper para mejorar el colchón</h3>
<p>Si el colchón de la camper es demasiado firme, un topper plegable puede mejorar mucho el descanso y guardarse cuando no se utiliza.</p>
<h3>2. Almohadas compactas</h3>
<p>Las almohadas de viaje o modelos comprimibles ocupan menos espacio que una almohada convencional y resultan prácticas cuando el almacenamiento es limitado.</p>
<h3>3. Oscurecer correctamente las ventanas</h3>
<p>Los oscurecedores térmicos para cabina y ventanas ayudan a reducir la entrada de luz y también pueden aportar aislamiento frente al frío y el calor.</p>
<h3>4. Ropa de cama adecuada</h3>
<p>Un saco nórdico, manta ligera o sistema de cama diseñado para espacios pequeños permite adaptar el descanso a la temperatura sin ocupar medio armario.</p>
<h3>5. Ventilación durante la noche</h3>
<p>Dormir con una ventilación adecuada ayuda a reducir la condensación. En función del vehículo, una pequeña apertura protegida puede ser suficiente.</p>
<h3>6. Menos ruido, más descanso</h3>
<p>Tapones reutilizables y accesorios sencillos para reducir el ruido exterior pueden marcar la diferencia cuando se duerme en un camping concurrido.</p>
<h3>7. Tener todo a mano</h3>
<p>Un pequeño organizador junto a la cama permite guardar gafas, móvil, cargador, llaves y otros objetos sin tener que levantarse constantemente.</p>
<h3>Accesorios que pueden ayudarte</h3>
<ul>
<li><a href="https://www.amazon.es/s?k=topper+plegable+camper&tag=caravaning0a-21" target="_blank" rel="nofollow sponsored noopener">Topper plegable para camper</a></li>
<li><a href="https://www.amazon.es/s?k=almohada+viaje+compacta&tag=caravaning0a-21" target="_blank" rel="nofollow sponsored noopener">Almohada compacta de viaje</a></li>
<li><a href="https://www.amazon.es/s?k=oscurecedores+termicos+camper&tag=caravaning0a-21" target="_blank" rel="nofollow sponsored noopener">Oscurecedores térmicos para camper</a></li>
<li><a href="https://www.amazon.es/s?k=organizador+cama+camper&tag=caravaning0a-21" target="_blank" rel="nofollow sponsored noopener">Organizador para la zona de cama</a></li>
</ul>
<p><strong>Consejo:</strong> antes de comprar, mide el espacio disponible y comprueba que el accesorio pueda guardarse fácilmente cuando la cama tenga que convertirse de nuevo en zona de día.</p>
<hr>
<p><small>Este artículo puede incluir enlaces de afiliado. En calidad de Afiliado de Amazon, obtenemos ingresos por las compras adscritas que cumplen los requisitos aplicables, sin coste adicional para ti.</small></p>
"""


def create_post(apps, schema_editor):
    Post = apps.get_model("blog", "Post")
    PostImage = apps.get_model("blog", "PostImage")

    post, created = Post.objects.get_or_create(
        slug=POST_SLUG,
        defaults={
            "title": "Accesorios para dormir mejor en una camper",
            "content": CONTENT,
            "meta_description": "Descubre accesorios prácticos para dormir mejor en una camper: topper, almohadas compactas, oscurecedores, ropa de cama y organizadores.",
            "status": "published",
        },
    )

    if not created:
        post.content = CONTENT
        post.meta_description = "Descubre accesorios prácticos para dormir mejor en una camper: topper, almohadas compactas, oscurecedores, ropa de cama y organizadores."
        post.status = "published"
        post.save(update_fields=["content", "meta_description", "status"])

    PostImage.objects.filter(post=post).delete()
    for image_url, _alt in IMAGES:
        PostImage.objects.create(post=post, image_url=image_url)


class Migration(migrations.Migration):
    dependencies = [("blog", "0043_corregir_imagenes_organizacion_autocaravana")]
    operations = [migrations.RunPython(create_post, migrations.RunPython.noop)]
