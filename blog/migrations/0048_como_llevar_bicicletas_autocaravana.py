from django.db import migrations

POST_SLUG = "como-llevar-bicicletas-autocaravana"
CONTENT = """
<h2>Cómo llevar bicicletas en una autocaravana</h2>
<p>Viajar con bicicletas abre muchas posibilidades cuando recorres destinos en autocaravana. El sistema adecuado depende del tipo de vehículo, del número de bicicletas y del peso que necesitas transportar.</p>
<h3>1. Portabicicletas trasero</h3>
<p>Es una de las soluciones más habituales. Se instala en la parte posterior de la autocaravana y permite llevar varias bicicletas sin ocupar el espacio interior.</p>
<h3>2. Portabicicletas para bola de remolque</h3>
<p>Si tu autocaravana dispone de bola homologada, un portabicicletas de plataforma puede resultar cómodo para cargar y descargar las bicicletas. Comprueba siempre la capacidad de carga y la compatibilidad con el vehículo.</p>
<h3>3. Llevar las bicicletas en el garaje</h3>
<p>Algunas autocaravanas tienen un garaje suficientemente amplio para transportar bicicletas en el interior. Es una opción que las protege mejor de la lluvia y de posibles robos, aunque hay que vigilar el peso total.</p>
<h3>4. ¿Y si son bicicletas eléctricas?</h3>
<p>Las bicicletas eléctricas suelen pesar bastante más que una bicicleta convencional. Antes de comprar el portabicicletas comprueba su carga máxima y la capacidad individual por bicicleta.</p>
<h3>5. Protege las bicicletas durante el viaje</h3>
<p>Utiliza correas adecuadas, protectores para cuadros y elementos que eviten que las bicicletas se golpeen entre sí. Una funda puede ayudar a protegerlas del polvo, barro y lluvia cuando el sistema sea compatible con ella.</p>
<h3>6. Seguridad y antirrobo</h3>
<p>Las correas de sujeción mantienen las bicicletas en su sitio, pero no sustituyen a un sistema antirrobo. Cuando aparques, utiliza un cable de seguridad o candado diseñado para este tipo de transporte.</p>
<h3>7. No olvides la visibilidad y la carga</h3>
<p>Comprueba que las bicicletas no oculten matrícula, luces o elementos obligatorios del vehículo. El conjunto debe quedar correctamente asegurado y respetar las limitaciones de peso y dimensiones.</p>
<h3>Accesorios que pueden ayudarte</h3>
<ul>
<li><a href="https://www.amazon.es/s?k=portabicicletas+autocaravana+4+bicicletas&tag=caravaning0a-21" target="_blank" rel="nofollow sponsored noopener">Portabicicletas para autocaravana</a></li>
<li><a href="https://www.amazon.es/s?k=cable+antirrobo+bicicleta+acero&tag=caravaning0a-21" target="_blank" rel="nofollow sponsored noopener">Cable antirrobo para bicicletas</a></li>
<li><a href="https://www.amazon.es/s?k=correas+sujecion+bicicletas+portabicicletas&tag=caravaning0a-21" target="_blank" rel="nofollow sponsored noopener">Correas de sujeción para bicicletas</a></li>
<li><a href="https://www.amazon.es/s?k=funda+bicicleta+portabicicletas&tag=caravaning0a-21" target="_blank" rel="nofollow sponsored noopener">Funda para bicicleta</a></li>
</ul>
<p><strong>Consejo:</strong> pesa las bicicletas y el propio portabicicletas antes de cargarlo. En especial con bicicletas eléctricas, unos pocos kilos pueden cambiar bastante el margen disponible.</p>
<hr><p><small>Este artículo puede incluir enlaces de afiliado. En calidad de Afiliado de Amazon, obtenemos ingresos por las compras adscritas que cumplen los requisitos aplicables, sin coste adicional para ti.</small></p>
"""

IMAGES = [
    "https://images.pexels.com/photos/100582/pexels-photo-100582.jpeg?auto=compress&cs=tinysrgb&w=1200",
    "https://images.pexels.com/photos/276517/pexels-photo-276517.jpeg?auto=compress&cs=tinysrgb&w=1200",
    "https://images.pexels.com/photos/5807546/pexels-photo-5807546.jpeg?auto=compress&cs=tinysrgb&w=1200",
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
        post = Post.objects.create(
            slug=POST_SLUG,
            title="Cómo llevar bicicletas en una autocaravana",
            content=CONTENT,
            meta_description="Guía para llevar bicicletas en una autocaravana: portabicicletas, bicicletas eléctricas, seguridad, peso y accesorios.",
            status="PUBLISHED",
            author=author,
        )
    else:
        post.content = CONTENT
        post.meta_description = "Guía para llevar bicicletas en una autocaravana: portabicicletas, bicicletas eléctricas, seguridad, peso y accesorios."
        post.status = "PUBLISHED"
        post.save(update_fields=["content", "meta_description", "status"])
    PostImage.objects.filter(post=post).delete()
    for url in IMAGES:
        PostImage.objects.create(post=post, image_url=url)


class Migration(migrations.Migration):
    dependencies = [("blog", "0047_corregir_imagenes_viajar_camper_invierno")]
    operations = [migrations.RunPython(create_post, migrations.RunPython.noop)]
