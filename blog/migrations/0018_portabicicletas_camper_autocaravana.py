from django.db import migrations

POST_SLUG = "portabicicletas-camper-autocaravana"
TAG = "caravaning0a-21"

PRODUCTS = [
    {
        "name": "Fiamma Carry-Bike para autocaravana y camper",
        "query": "Fiamma Carry-Bike autocaravana camper",
        "image": "https://commons.wikimedia.org/wiki/Special:Redirect/file/Fahrradtr%C3%A4ger.JPG",
        "alt": "Portabicicletas montado en un vehículo recreativo",
        "type": "trasero para autocaravana o camper",
        "text": "Los sistemas Carry-Bike de Fiamma son una referencia habitual en el mundo del caravaning. La clave es elegir la versión compatible con la pared trasera y la distribución de tu vehículo. Antes de comprar, comprueba el modelo exacto, la distancia entre puntos de fijación y la carga máxima admitida.",
    },
    {
        "name": "Thule Elite Van XT",
        "query": "Thule Elite Van XT portabicicletas camper",
        "image": "https://commons.wikimedia.org/wiki/Special:Redirect/file/1977_Toyota_Truck_with_Chinook_camper%2C_front_right%2C_4-11-2021.jpg",
        "alt": "Camper con portabicicletas trasero",
        "type": "trasero para furgonetas camper",
        "text": "El Thule Elite Van XT está pensado para determinadas furgonetas y se instala en las puertas traseras sin necesidad de perforarlas en las configuraciones compatibles. Es especialmente interesante si quieres transportar dos bicicletas y conservar un acceso cómodo a las puertas. Thule indica una capacidad máxima de 35 kg en determinadas versiones, pero la compatibilidad depende del vehículo.",
    },
    {
        "name": "Peruzzo Pure Instinct para 2 bicicletas",
        "query": "Peruzzo Pure Instinct 2 bicicletas portabicicletas",
        "image": "https://commons.wikimedia.org/wiki/Special:Redirect/file/Kuat_Bike_Rack.jpg",
        "alt": "Portabicicletas de plataforma montado en la parte trasera de un vehículo",
        "type": "de bola de remolque",
        "text": "Los portabicicletas de bola son una opción muy interesante cuando la camper o el vehículo tractor dispone de enganche homologado. Suelen ser fáciles de cargar y permiten transportar bicicletas pesadas, incluidas muchas eléctricas, siempre que el conjunto respete la capacidad del portabicicletas y la carga vertical del enganche.",
    },
    {
        "name": "Atera Strada para enganche",
        "query": "Atera Strada portabicicletas enganche 2 bicicletas",
        "image": "https://commons.wikimedia.org/wiki/Special:Redirect/file/Atera_Strada_DL2_Fahrradtr%C3%A4ger.jpg",
        "alt": "Portabicicletas Atera Strada de enganche",
        "type": "de bola de remolque",
        "text": "Atera Strada es otra familia de portabicicletas de enganche conocida por sus soluciones para dos o más bicicletas. Puede ser una alternativa interesante para quienes prefieren una plataforma baja y cómoda para cargar las bicicletas. Comprueba siempre el número de bicicletas, el peso máximo y las dimensiones permitidas.",
    },
    {
        "name": "Menabo Mistral para transporte trasero",
        "query": "Menabo Mistral portabicicletas trasero",
        "image": "https://commons.wikimedia.org/wiki/Special:Redirect/file/Fahrradtraeger.jpg",
        "alt": "Portabicicletas trasero para vehículo",
        "type": "trasero para vehículo compatible",
        "text": "Menabo ofrece soluciones de transporte de bicicletas de diferentes formatos. Puede resultar interesante para presupuestos más contenidos, pero en una camper hay que prestar especial atención a la compatibilidad con la carrocería, la visibilidad de matrícula y pilotos y la capacidad de carga real del sistema.",
    },
]


def amazon_url(query):
    return "https://www.amazon.es/s?k=" + query.replace(" ", "+") + "&tag=" + TAG


def build_post(apps, schema_editor):
    Post = apps.get_model("blog", "Post")
    PostImage = apps.get_model("blog", "PostImage")
    User = apps.get_model("auth", "User")

    author = User.objects.filter(username="miguel").first() or User.objects.filter(is_superuser=True).first()
    if not author:
        return

    post, created = Post.objects.get_or_create(
        slug=POST_SLUG,
        defaults={
            "author": author,
            "title": "Portabicicletas para camper y autocaravana: 5 opciones que merece la pena mirar",
            "meta_description": "Guía para elegir portabicicletas para camper y autocaravana. Comparamos opciones traseras, de bola y para furgoneta y explicamos qué debes comprobar antes de comprar.",
            "content": "",
            "status": "PUBLISHED",
        },
    )

    post.author = author
    post.title = "Portabicicletas para camper y autocaravana: 5 opciones que merece la pena mirar"
    post.meta_description = "Guía para elegir portabicicletas para camper y autocaravana. Comparamos opciones traseras, de bola y para furgoneta y explicamos qué debes comprobar antes de comprar."
    post.status = "PUBLISHED"

    cover = "https://commons.wikimedia.org/wiki/Special:Redirect/file/1977_Toyota_Truck_with_Chinook_camper%2C_front_right%2C_4-11-2021.jpg"
    body = f'''
<p><strong>Si viajas en camper o autocaravana y también quieres llevar bicicletas, el portabicicletas deja de ser un accesorio secundario y se convierte en parte del equipamiento del viaje.</strong> El problema es que no todos los sistemas sirven para todos los vehículos: hay modelos para pared trasera, puertas de furgoneta, bola de remolque y otras configuraciones específicas.</p>
<p>En esta guía hemos reunido cinco opciones y familias de producto que merece la pena mirar en Amazon España. No nos fijamos únicamente en el precio: también importa la compatibilidad, el peso de las bicicletas, el acceso a las puertas y la facilidad de carga.</p>
<div style="margin:24px 0;padding:18px;border-radius:16px;background:#f5f5f5;"><strong>🚲 Antes de comprar:</strong> comprueba siempre el modelo exacto de tu camper/autocaravana, el número y peso de las bicicletas, la carga máxima del sistema y las instrucciones del fabricante. En bicicletas eléctricas, el peso de cada unidad es especialmente importante.</div>
<h2>¿Qué tipo de portabicicletas necesitas?</h2>
<p>La primera decisión es el sistema de montaje. En una autocaravana suele ser habitual el montaje trasero específico para vehículos recreativos. En una furgoneta camper pueden existir soluciones para puertas traseras. Si tienes una bola de remolque homologada, una plataforma de enganche puede ser una opción muy cómoda.</p>
<p>También conviene pensar en cómo utilizas las bicicletas. Dos bicicletas ligeras para excursiones ocasionales no plantean las mismas exigencias que dos bicicletas eléctricas pesadas utilizadas durante todo el año.</p>
'''

    for index, product in enumerate(PRODUCTS, start=1):
        link = amazon_url(product["query"])
        body += f'''
<h2>{index}. {product["name"]}</h2>
<p>{product["text"]}</p>
<p><strong>Tipo:</strong> {product["type"]}.</p>
<img src="{product["image"]}" alt="{product["alt"]}" loading="lazy" style="display:block;width:100%;max-width:100%;aspect-ratio:16/9;height:auto;object-fit:cover;border-radius:16px;margin:18px 0;">
<p><em>Imagen ilustrativa del sistema de transporte de bicicletas. La fotografía no representa necesariamente el modelo exacto enlazado.</em></p>
<p><a href="{link}" target="_blank" rel="nofollow sponsored noopener" style="display:inline-block;padding:12px 18px;border-radius:10px;background:#ff9900;color:#111;text-decoration:none;font-weight:700;">🛒 Ver opciones de {product["name"]} en Amazon</a></p>
'''

    body += '''
<h2>5 cosas que debes comprobar antes de comprar</h2>
<h3>1. Peso máximo</h3>
<p>No te fijes solo en cuántas bicicletas caben. Comprueba el peso máximo total y el peso permitido por bicicleta. Una bicicleta eléctrica puede pesar bastante más que una bicicleta convencional.</p>
<h3>2. Compatibilidad con tu vehículo</h3>
<p>Que un portabicicletas sea para camper no significa que sea válido para cualquier camper. En sistemas de pared o puerta trasera hay que comprobar medidas, puntos de fijación y compatibilidad con el vehículo.</p>
<h3>3. Acceso a puertas, garaje y maletero</h3>
<p>Antes de comprar, piensa qué ocurre cuando necesitas abrir el garaje trasero o las puertas. Algunos sistemas permiten bascular o retirar parte del conjunto; otros requieren desmontar las bicicletas.</p>
<h3>4. Bicicletas eléctricas</h3>
<p>Si transportas e-bikes, revisa especialmente el peso. También es recomendable retirar las baterías durante el transporte cuando el fabricante de la bicicleta y del portabicicletas así lo indiquen.</p>
<h3>5. Matrícula, luces y carga trasera</h3>
<p>La instalación puede afectar a la visibilidad de la matrícula y de las luces. Si el sistema las tapa, puede ser necesario utilizar una solución homologada de repetición de matrícula y alumbrado. Consulta siempre la normativa aplicable y las instrucciones del fabricante antes de circular.</p>

<h2>¿Portabicicletas de pared o de bola?</h2>
<p>Para una autocaravana con puntos de fijación compatibles, un sistema trasero específico puede integrarse muy bien con el vehículo. En cambio, una plataforma de bola suele ser muy cómoda para cargar las bicicletas a una altura más baja y puede ser especialmente interesante para bicicletas pesadas.</p>
<p>En una furgoneta camper, los sistemas específicos para puertas traseras pueden ser una solución limpia, pero la compatibilidad con el modelo exacto de furgoneta es fundamental.</p>

<h2>Nuestra recomendación</h2>
<p>Si ya tienes una autocaravana preparada para un sistema trasero, empezaría buscando una solución específica de fabricantes especializados como Fiamma. Si tienes una furgoneta camper compatible con un sistema de puerta trasera, merece la pena mirar opciones como Thule. Y si dispones de bola de remolque homologada, compararía plataformas de enganche antes de decidirme.</p>
<p>La mejor compra no es necesariamente el portabicicletas más barato: es el que encaja correctamente con tu vehículo, soporta tus bicicletas y te permite utilizarlas sin convertir cada parada en una operación de ingeniería.</p>

<div style="margin:30px 0;padding:16px;border:1px solid #ddd;border-radius:12px;"><strong>Nota de afiliación:</strong> Algunos enlaces de este artículo son enlaces de afiliado. Si realizas una compra después de acceder a ellos, Caravaning Project puede recibir una comisión sin que esto suponga un coste adicional para ti. Los precios y la disponibilidad pueden cambiar.</div>

<h2>Preguntas frecuentes</h2>
<h3>¿Puedo llevar bicicletas eléctricas en cualquier portabicicletas?</h3>
<p>No. Debes comprobar el peso máximo permitido por bicicleta y la capacidad total del sistema. Algunos modelos están preparados para e-bikes y otros no.</p>
<h3>¿Es mejor un portabicicletas de bola?</h3>
<p>No siempre. Si tu vehículo no dispone de bola o necesitas una solución integrada en la parte trasera de una autocaravana, un sistema específico puede ser más adecuado.</p>
<h3>¿Tengo que quitar las baterías de las bicicletas eléctricas?</h3>
<p>Depende de las instrucciones de la bicicleta, del fabricante del portabicicletas y de las condiciones del transporte. Comprueba siempre las recomendaciones de ambos fabricantes.</p>
<h3>¿Puedo abrir las puertas con las bicicletas montadas?</h3>
<p>Depende completamente del sistema y del vehículo. Algunas soluciones están diseñadas precisamente para mantener el acceso, mientras que otras requieren retirar o bascular el portabicicletas.</p>

<h2>Conclusión</h2>
<p>Llevar las bicicletas contigo cambia por completo las posibilidades de una escapada en camper o autocaravana. Una ruta junto al mar, una vía verde o una visita a un pueblo cercano pueden estar a solo unos kilómetros del camping.</p>
<p>Antes de comprar, mide, pesa y comprueba la compatibilidad. Después, elige el sistema que mejor encaje con tu forma de viajar.</p>

<hr>
<h3>📷 Créditos de las fotografías</h3>
<p>Las imágenes utilizadas en esta guía proceden de Wikimedia Commons y se emplean como fotografías ilustrativas del tipo de sistema descrito. La fotografía de la camper con portabicicletas es una imagen de dominio público; otras fotografías proceden de Wikimedia Commons bajo licencias Creative Commons. Las imágenes no implican que el producto mostrado sea exactamente el producto enlazado en Amazon.</p>
'''

    post.content = body
    post.save()

    PostImage.objects.filter(post=post).delete()
    PostImage.objects.create(post=post, image_url=cover)
    for product in PRODUCTS:
        PostImage.objects.get_or_create(post=post, image_url=product["image"])


def reverse_build_post(apps, schema_editor):
    pass


class Migration(migrations.Migration):
    dependencies = [("blog", "0017_fotos_productos_reales_cc")]
    operations = [migrations.RunPython(build_post, reverse_build_post)]
