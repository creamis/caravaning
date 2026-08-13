from django.db import migrations

POST_SLUG = "accesorios-dormir-mejor-camper"

IMAGES = [
    ("https://www.outsideonline.com/wp-content/uploads/2023/05/van-life-interior-storage_h.jpg", "Interior de camper preparado como zona de descanso"),
    ("https://www.campervanlife.com/wp-content/uploads/2024/01/campervan-storage-interior.jpg", "Zona de descanso y almacenamiento en una campervan"),
    ("https://vandoit.com/wp-content/uploads/2023/03/40435-25-of-37.jpg", "Interior de campervan preparado para dormir durante un viaje"),
]

CONTENT = """
<h2>Accesorios para dormir mejor en una camper</h2>
<p>Dormir en una camper puede ser una de las mejores partes del viaje, pero una cama incómoda, demasiada luz o falta de ventilación pueden convertir la noche en una pequeña batalla. Con algunos accesorios bien elegidos puedes ganar comodidad sin llenar de trastos el vehículo.</p>
<h3>1. Un buen topper para mejorar el colchón</h3><p>Si el colchón de la camper es demasiado firme, un topper plegable puede mejorar mucho el descanso y guardarse cuando no se utiliza.</p>
<h3>2. Almohadas compactas</h3><p>Las almohadas de viaje o modelos comprimibles ocupan menos espacio que una almohada convencional y resultan prácticas cuando el almacenamiento es limitado.</p>
<h3>3. Oscurecer correctamente las ventanas</h3><p>Los oscurecedores térmicos para cabina y ventanas ayudan a reducir la entrada de luz y también pueden aportar aislamiento frente al frío y el calor.</p>
<h3>4. Ropa de cama adecuada</h3><p>Un saco nórdico, manta ligera o sistema de cama diseñado para espacios pequeños permite adaptar el descanso a la temperatura sin ocupar medio armario.</p>
<h3>5. Ventilación durante la noche</h3><p>Dormir con una ventilación adecuada ayuda a reducir la condensación. En función del vehículo, una pequeña apertura protegida puede ser suficiente.</p>
<h3>6. Menos ruido, más descanso</h3><p>Tapones reutilizables y accesorios sencillos para reducir el ruido exterior pueden marcar la diferencia cuando se duerme en un camping concurrido.</p>
<h3>7. Tener todo a mano</h3><p>Un pequeño organizador junto a la cama permite guardar gafas, móvil, cargador, llaves y otros objetos sin tener que levantarse constantemente.</p>
<h3>Accesorios que pueden ayudarte</h3>
<ul>
<li><a href="https://www.amazon.es/s?k=topper+plegable+camper&tag=caravaning0a-21" target="_blank" rel="nofollow sponsored noopener">Topper plegable para camper</a></li>
<li><a href="https://www.amazon.es/s?k=almohada+viaje+compacta&tag=caravaning0a-21" target="_blank" rel="nofollow sponsored noopener">Almohada compacta de viaje</a></li>
<li><a href="https://www.amazon.es/s?k=oscurecedores+termicos+camper&tag=caravaning0a-21" target="_blank" rel="nofollow sponsored noopener">Oscurecedores térmicos para camper</a></li>
<li><a href="https://www.amazon.es/s?k=organizador+cama+camper&tag=caravaning0a-21" target="_blank" rel="nofollow sponsored noopener">Organizador para la zona de cama</a></li>
</ul>
<p><strong>Consejo:</strong> antes de comprar, mide el espacio disponible y comprueba que el accesorio pueda guardarse fácilmente cuando la cama tenga que convertirse de nuevo en zona de día.</p>
<hr><p><small>Este artículo puede incluir enlaces de afiliado. En calidad de Afiliado de Amazon, obtenemos ingresos por las compras adscritas que cumplen los requisitos aplicables, sin coste adicional para ti.</small></p>
"""


def create_post(apps, schema_editor):
    Post = apps.get_model("blog", "Post")
    User = apps.get_model("auth", "User")
    PostImage = apps.get_model("blog", "PostImage")

    post = Post.objects.filter(slug=POST_SLUG).first()
    if post:
        post.content = CONTENT
        post.meta_description = "Descubre accesorios prácticos para dormir mejor en una camper: topper, almohadas compactas, oscurecedores, ropa de cama y organizadores."
        post.status = "PUBLISHED"
        post.save(update_fields=["content", "meta_description", "status"])
    else:
        author = User.objects.order_by("id").first()
        if not author:
            return
        post = Post.objects.create(
            slug=POST_SLUG,
            title="Accesorios para dormir mejor en una camper",
            content=CONTENT,
            meta_description="Descubre accesorios prácticos para dormir mejor en una camper: topper, almohadas compactas, oscurecedores, ropa de cama y organizadores.",
            status="PUBLISHED",
            author=author,
        )

    PostImage.objects.filter(post=post).delete()
    for image_url, _alt in IMAGES:
        PostImage.objects.create(post=post, image_url=image_url)


class Migration(migrations.Migration):
    dependencies = [("blog", "0043_corregir_imagenes_organizacion_autocaravana")]
    operations = [migrations.RunPython(create_post, migrations.RunPython.noop)]
