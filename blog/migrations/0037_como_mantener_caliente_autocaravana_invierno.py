from django.db import migrations
from urllib.parse import quote_plus

POST_SLUG = "como-mantener-caliente-autocaravana-invierno"
TAG = "caravaning0a-21"
IMAGES = [
    ("https://images.unsplash.com/photo-1601918774946-25832a4be0d6?auto=format&fit=crop&w=1600&q=85", "Autocaravana camper preparada para una escapada de invierno"),
    ("https://images.unsplash.com/photo-1544986581-efac024faf62?auto=format&fit=crop&w=1400&q=85", "Interior acogedor de una autocaravana en invierno"),
    ("https://images.unsplash.com/photo-1510798831971-661eb04b3739?auto=format&fit=crop&w=1400&q=85", "Control de temperatura y ambiente interior"),
]

def amazon(query):
    return f"https://www.amazon.es/s?k={quote_plus(query)}&tag={TAG}"

def update_post(apps, schema_editor):
    Post = apps.get_model("blog", "Post")
    PostImage = apps.get_model("blog", "PostImage")
    User = apps.get_model("auth", "User")
    author = User.objects.filter(username="miguel").first() or User.objects.filter(is_superuser=True).order_by("id").first()
    if not author:
        return
    post, _ = Post.objects.get_or_create(slug=POST_SLUG, defaults={"title": "Cómo mantener caliente una autocaravana en invierno", "author": author, "status": "PUBLISHED", "content": ""})
    post.title = "Cómo mantener caliente una autocaravana en invierno"
    post.author = author
    post.status = "PUBLISHED"
    PostImage.objects.filter(post=post).delete()
    for url, _alt in IMAGES:
        PostImage.objects.create(post=post, image_url=url)
    links = {
        "cortinas": amazon("cortinas termicas autocaravana camper"),
        "burletes": amazon("burlete aislante puerta autocaravana camper"),
        "termometro": amazon("termometro higrometro digital camper autocaravana"),
        "alfombra": amazon("alfombra termica camper autocaravana"),
    }
    post.content = f'''<p>Viajar en autocaravana durante los meses fríos puede ser una auténtica maravilla si el interior está bien preparado. La clave no consiste únicamente en subir la calefacción: también hay que evitar que el calor se escape y controlar la humedad.</p>
<h2>1. Empieza por las ventanas y la cabina</h2><p>Las ventanas y el parabrisas son superficies especialmente expuestas al exterior. Un buen aislamiento específico para la cabina ayuda a reducir la pérdida de temperatura y además aporta privacidad.</p><p><a href="{links['cortinas']}" target="_blank" rel="nofollow sponsored noopener"><strong>🛒 Ver cortinas y aislantes térmicos para camper en Amazon</strong></a></p>
<h2>2. Revisa puertas y pequeñas entradas de aire</h2><p>Comprueba juntas, puertas y compartimentos exteriores y sustituye los burletes deteriorados.</p><p><a href="{links['burletes']}" target="_blank" rel="nofollow sponsored noopener"><strong>🛒 Ver burletes aislantes para puertas y ventanas en Amazon</strong></a></p>
<h2>3. Controla la humedad</h2><p>En invierno respiramos, cocinamos y utilizamos agua dentro de un espacio reducido. La humedad puede condensarse sobre las superficies frías, por lo que conviene ventilar brevemente y mantenerla controlada.</p><p><a href="{links['termometro']}" target="_blank" rel="nofollow sponsored noopener"><strong>🛒 Ver termómetros e higrómetros digitales en Amazon</strong></a></p>
<h2>4. No olvides el suelo</h2><p>Una alfombra adecuada para camper ayuda a mejorar el confort y hace más agradable permanecer dentro durante la noche.</p><p><a href="{links['alfombra']}" target="_blank" rel="nofollow sponsored noopener"><strong>🛒 Ver alfombras y soluciones térmicas para camper en Amazon</strong></a></p>
<h2>5. Utiliza la calefacción de forma eficiente</h2><p>Utiliza la calefacción siguiendo las instrucciones del fabricante y mantén una ventilación correcta. No bloquees las salidas de aire y presta especial atención a los sistemas de seguridad cuando utilices aparatos de combustión.</p>
<h2>6. Cocina y ventila con cabeza</h2><p>Cocinar dentro genera vapor y humedad. Ventilar unos minutos después de cocinar ayuda a controlar la condensación.</p>
<h2>7. Antes de dormir</h2><ul><li>Cierra correctamente las cortinas y aislantes.</li><li>Comprueba puertas y ventanas.</li><li>No bloquees las salidas de calefacción.</li><li>Controla temperatura y humedad.</li><li>Prepara ropa de cama adecuada.</li></ul>
<h2>¿Cuánto aislamiento necesitas?</h2><p>Depende del vehículo, del clima y de la frecuencia con la que viajes en invierno. Si todavía no tienes aislada la cabina, suele ser un buen primer paso y después puedes ampliar a las ventanas del habitáculo.</p>
<h2>También te puede interesar</h2><p>Para profundizar en el aislamiento, consulta nuestra guía <strong>Los mejores aislantes térmicos para camper</strong>.</p>
<p><em>Este artículo puede incluir enlaces de afiliado. En calidad de Afiliado de Amazon, obtengo ingresos por las compras adscritas que cumplen los requisitos aplicables, sin coste adicional para ti.</em></p>'''
    post.meta_description = "Consejos prácticos para mantener caliente una autocaravana en invierno: aislamiento, ventanas, puertas, humedad, suelo y calefacción eficiente."
    post.save()

class Migration(migrations.Migration):
    dependencies = [("blog", "0036_completar_aislantes_termicos_camper")]
    operations = [migrations.RunPython(update_post, migrations.RunPython.noop)]
