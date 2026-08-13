from django.db import migrations

POST_SLUG = "viajar-camper-invierno"
CONTENT = """
<h2>Qué necesitas para viajar con una camper en invierno</h2>
<p>Viajar en camper durante los meses fríos permite descubrir carreteras y paisajes con mucha menos gente, pero requiere preparar el vehículo y el equipaje de otra manera. Con el equipo adecuado puedes mantener el interior confortable y viajar con seguridad incluso cuando bajan las temperaturas.</p>
<h3>1. Aislamiento térmico</h3>
<p>Un buen aislamiento en ventanas y zonas sensibles reduce la pérdida de calor y ayuda a evitar la condensación. Los oscurecedores térmicos son especialmente útiles en la cabina.</p>
<h3>2. Calefacción y ventilación</h3>
<p>La calefacción es importante, pero también lo es ventilar correctamente. Una pequeña renovación de aire ayuda a controlar la humedad y la condensación durante la noche.</p>
<h3>3. Ropa adecuada</h3>
<p>Conviene llevar varias capas, ropa térmica, calcetines calientes, gorro y calzado preparado para lluvia o frío. Vestirse por capas permite adaptarse mejor a los cambios de temperatura.</p>
<h3>4. Protección del agua</h3>
<p>Si vas a viajar por zonas con temperaturas bajo cero, presta especial atención al depósito, tuberías y puntos de suministro. El riesgo de congelación aumenta durante las noches más frías.</p>
<h3>5. Electricidad y batería</h3>
<p>La calefacción y otros equipos pueden aumentar el consumo eléctrico. Comprueba el estado de la batería y lleva cables y adaptadores adecuados para los campings que visites.</p>
<h3>6. Cocina para días fríos</h3>
<p>Una pequeña cocina bien organizada permite preparar comidas calientes sin depender siempre de restaurantes. Lleva utensilios compactos y alimentos fáciles de conservar.</p>
<h3>7. Seguridad en carretera</h3>
<p>Antes de salir comprueba neumáticos, líquidos, limpiaparabrisas y luces. Si existe posibilidad de nieve o hielo, consulta el estado de las carreteras y lleva el equipamiento obligatorio que corresponda.</p>
<h3>8. Accesorios que pueden ser útiles</h3>
<ul>
<li><a href="https://www.amazon.es/s?k=oscurecedores+termicos+camper&tag=caravaning0a-21" target="_blank" rel="nofollow sponsored noopener">Oscurecedores térmicos para camper</a></li>
<li><a href="https://www.amazon.es/s?k=calefaccion+12v+camper&tag=caravaning0a-21" target="_blank" rel="nofollow sponsored noopener">Calefacción portátil para camper</a></li>
<li><a href="https://www.amazon.es/s?k=termometro+higrometro+camper&tag=caravaning0a-21" target="_blank" rel="nofollow sponsored noopener">Termómetro e higrómetro</a></li>
<li><a href="https://www.amazon.es/s?k=manta+termica+camper&tag=caravaning0a-21" target="_blank" rel="nofollow sponsored noopener">Manta térmica para viajes</a></li>
</ul>
<p><strong>Consejo:</strong> antes de salir revisa la previsión meteorológica y adapta la ruta. En invierno, disponer de margen para cambiar de destino puede ser tan importante como llevar más equipamiento.</p>
<hr><p><small>Este artículo puede incluir enlaces de afiliado. En calidad de Afiliado de Amazon, obtenemos ingresos por las compras adscritas que cumplen los requisitos aplicables, sin coste adicional para ti.</small></p>
"""

IMAGES = [
    "https://www.pexels.com/photo/camper-van-in-snowy-mountains-15346718/",
    "https://www.pexels.com/photo/camper-van-parked-in-winter-landscape-18934491/",
    "https://www.pexels.com/photo/camper-van-in-a-snowy-landscape-16496749/",
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
        post = Post.objects.create(slug=POST_SLUG, title="Qué necesitas para viajar con una camper en invierno", content=CONTENT, meta_description="Todo lo que necesitas para viajar con una camper en invierno: aislamiento, calefacción, ropa, agua, electricidad y seguridad.", status="PUBLISHED", author=author)
    else:
        post.content = CONTENT
        post.meta_description = "Todo lo que necesitas para viajar con una camper en invierno: aislamiento, calefacción, ropa, agua, electricidad y seguridad."
        post.status = "PUBLISHED"
        post.save(update_fields=["content", "meta_description", "status"])
    PostImage.objects.filter(post=post).delete()
    for url in IMAGES:
        PostImage.objects.create(post=post, image_url=url)

class Migration(migrations.Migration):
    dependencies = [("blog", "0045_imagenes_dormir_camper_wikimedia")]
    operations = [migrations.RunPython(create_post, migrations.RunPython.noop)]
