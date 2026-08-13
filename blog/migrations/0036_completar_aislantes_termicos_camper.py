from django.db import migrations
from urllib.parse import quote_plus

POST_SLUG = "mejores-aislantes-termicos-camper"
TAG = "caravaning0a-21"
IMAGES = [
    ("https://www.getcamping.se/images/2x/list/8530-7405_hindermann_isoleringsmatta_husbil_universal.jpg", "Aislante térmico exterior Hindermann instalado en una autocaravana"),
    ("https://www.waerchzueg.ch/cdn/shop/products/thermo12_1200x.png?v=1758012916", "Aislante térmico multicapa instalado en la cabina de una camper"),
    ("https://littlemakes.com/img/image0_camper-insulation-ideas_reflective-window-covers.jpg", "Aislante reflectante colocado en una ventana lateral de una camper"),
]

def amazon(query):
    return f"https://www.amazon.es/s?k={quote_plus(query)}&tag={TAG}"

def update_post(apps, schema_editor):
    Post = apps.get_model("blog", "Post")
    PostImage = apps.get_model("blog", "PostImage")
    post = Post.objects.filter(slug=POST_SLUG).first()
    if not post:
        return
    PostImage.objects.filter(post=post).delete()
    for url, _alt in IMAGES:
        PostImage.objects.create(post=post, image_url=url)
    links = {
        "hindermann": amazon("Hindermann aislante termico autocaravana"),
        "multicapa": amazon("aislante multicapa camper autocaravana"),
        "ventanas": amazon("aislante termico camper autocaravana ventanas"),
        "parabrisas": amazon("aislante termico parabrisas camper autocaravana"),
    }
    post.content = f'''<p>Si quieres viajar en camper durante todo el año, el aislamiento térmico es una de las mejoras más sencillas para aumentar el confort. Las ventanas y la cabina pueden convertirse en puntos importantes de intercambio de temperatura, especialmente durante las noches frías.</p>
<h2>¿Qué hace realmente un aislante térmico?</h2>
<p>Un aislante crea una barrera adicional entre el interior y el exterior. Las soluciones reflectantes y multicapa también ayudan a reducir el intercambio de radiación y la entrada directa de luz solar.</p>
<h2>1. Aislantes exteriores para la cabina</h2>
<p>Los aislantes exteriores son especialmente interesantes para el parabrisas y las ventanas delanteras. Además de ayudar frente al frío, protegen el interior del sol y aportan privacidad cuando estamos estacionados.</p>
<p><a href="{links['hindermann']}" target="_blank" rel="nofollow sponsored noopener"><strong>🛒 Ver opciones de aislantes Hindermann para autocaravana en Amazon</strong></a></p>
<h2>2. Aislantes interiores multicapa</h2>
<p>Son una alternativa práctica para quienes montan y desmontan el aislamiento con frecuencia. Muchos utilizan varias capas de materiales reflectantes y aislantes y se fijan mediante ventosas, velcro o sistemas específicos.</p>
<p><a href="{links['multicapa']}" target="_blank" rel="nofollow sponsored noopener"><strong>🛒 Ver aislantes multicapa para camper y autocaravana en Amazon</strong></a></p>
<h2>3. Aislantes específicos para ventanas</h2>
<p>Las ventanas laterales son otro punto donde merece la pena actuar. Una solución ajustada al tamaño de cada ventana suele funcionar mejor que una lámina suelta, porque reduce las zonas descubiertas y mejora también el oscurecimiento.</p>
<p><a href="{links['ventanas']}" target="_blank" rel="nofollow sponsored noopener"><strong>🛒 Ver aislantes térmicos para ventanas de camper en Amazon</strong></a></p>
<h2>4. ¿Interior o exterior?</h2>
<table class="table table-bordered align-middle"><thead><tr><th>Tipo</th><th>Ventaja principal</th><th>Ideal para</th></tr></thead><tbody><tr><td><strong>Interior</strong></td><td>Montaje rápido y fácil de guardar</td><td>Escapadas frecuentes</td></tr><tr><td><strong>Exterior</strong></td><td>Protege también frente al sol y la intemperie</td><td>Invierno y estacionamientos prolongados</td></tr><tr><td><strong>Multicapa</strong></td><td>Buen equilibrio entre aislamiento y peso</td><td>Uso durante todo el año</td></tr></tbody></table>
<h2>5. Qué comprobar antes de comprar</h2><ul><li><strong>Compatibilidad:</strong> marca, modelo y año del vehículo.</li><li><strong>Medidas:</strong> comprueba las dimensiones reales.</li><li><strong>Fijación:</strong> ventosas, velcro, imanes o correas.</li><li><strong>Almacenamiento:</strong> en una camper cada centímetro cuenta.</li><li><strong>Uso:</strong> invierno, verano o todo el año.</li></ul>
<p><a href="{links['parabrisas']}" target="_blank" rel="nofollow sponsored noopener"><strong>🛒 Ver aislantes para parabrisas de camper y autocaravana en Amazon</strong></a></p>
<h2>Consejo final</h2><p>El mejor aislante no tiene por qué ser el más caro. Lo importante es que cubra correctamente la superficie, se adapte al vehículo y resulte cómodo de utilizar.</p>
<h2>También te puede interesar</h2><p>Si estás preparando una escapada en temporada fría, consulta también nuestra próxima guía sobre <strong>cómo mantener caliente una autocaravana en invierno</strong>.</p>
<p><em>Este artículo puede incluir enlaces de afiliado. En calidad de Afiliado de Amazon, obtengo ingresos por las compras adscritas que cumplen los requisitos aplicables, sin coste adicional para ti.</em></p>'''
    post.meta_description = "Descubre qué aislantes térmicos para camper y autocaravana elegir, diferencias entre modelos interiores y exteriores y consejos para mantener el confort todo el año."
    post.status = "PUBLISHED"
    post.save(update_fields=["content", "meta_description", "status", "updated_at"])

class Migration(migrations.Migration):
    dependencies = [("blog", "0035_aislantes_termicos_camper")]
    operations = [migrations.RunPython(update_post, migrations.RunPython.noop)]
