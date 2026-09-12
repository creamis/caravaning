from django.db import migrations

POST_SLUG = "guia-instalacion-solar-autocaravanas"

CONTENT = """
<p>Instalar placas solares en una autocaravana puede darte mucha más autonomía, pero una buena instalación empieza antes de subir al techo: hay que calcular el consumo, dimensionar paneles, regulador y batería, proteger correctamente el cableado y planificar la fijación y el paso de cables.</p>

<p>Esta guía explica el proceso de forma práctica para entender qué necesitas y en qué orden debes plantearlo. Si no tienes experiencia trabajando con instalaciones eléctricas de 12 V, baterías o pasos estancos en el techo, es recomendable que la parte crítica de la instalación la revise un profesional.</p>

<h2>1. Calcula primero cuánto consumes</h2>
<p>No elijas la placa únicamente por los vatios anunciados. Haz una lista de los equipos que utilizas cada día: nevera, iluminación LED, bomba de agua, móviles, portátil, televisión, ventilación y cualquier aparato conectado mediante inversor.</p>
<p>Una forma sencilla de calcular la energía diaria es:</p>
<p><strong>Consumo diario (Wh) = potencia del aparato (W) × horas de uso.</strong></p>
<p>Suma todos los consumos y deja margen para pérdidas y días con menor producción solar. La producción cambia mucho con la estación, la ubicación, la temperatura, las sombras y la orientación del vehículo.</p>

<h2>2. Componentes de una instalación solar para autocaravana</h2>
<ul>
<li><strong>Panel solar:</strong> transforma la radiación solar en electricidad.</li>
<li><strong>Regulador de carga:</strong> controla la energía que llega a la batería. Un MPPT suele aprovechar mejor la producción disponible que un PWM, especialmente cuando las condiciones solares no son ideales.</li>
<li><strong>Batería auxiliar:</strong> almacena la energía para utilizarla cuando no hay sol.</li>
<li><strong>Fusibles y protecciones:</strong> protegen el cableado y los equipos frente a sobrecorrientes y cortocircuitos.</li>
<li><strong>Cableado y conectores:</strong> deben dimensionarse según corriente, longitud y características del sistema.</li>
<li><strong>Pasacables y sellado:</strong> permiten entrar desde el techo al habitáculo evitando filtraciones.</li>
<li><strong>Inversor, si lo necesitas:</strong> convierte los 12 V de la batería en 230 V para determinados aparatos. No es imprescindible en todas las instalaciones.</li>
</ul>

<h2>3. ¿Panel rígido o flexible?</h2>
<p>Los paneles rígidos son una opción habitual en autocaravanas porque son resistentes y, montados con separación respecto al techo, permiten circulación de aire por debajo. Los flexibles son más ligeros y bajos, pero su montaje y disipación térmica requieren especial atención.</p>
<p>Antes de comprar mide el espacio real disponible entre claraboyas, antenas, aire acondicionado y otros elementos del techo. También conviene dejar margen para mantenimiento y una posible ampliación futura.</p>

<h2>4. Planifica la posición antes de fijar nada</h2>
<p>Presenta el panel y los soportes sin pegarlos. Comprueba que no interfieren con claraboyas y que las sombras de antenas u otros elementos no caen sobre el panel durante buena parte del día.</p>
<p>Decide también dónde estará el pasacables. Cuanto más razonable sea el recorrido hasta el regulador y la batería, más fácil será dimensionar y proteger correctamente el cableado.</p>

<h2>5. Fijación y sellado del panel</h2>
<p>La fijación debe ser compatible con el tipo de techo y con las indicaciones del fabricante del panel, los soportes y el adhesivo o sistema de anclaje empleado. La preparación de la superficie es fundamental: limpiar, desengrasar y respetar imprimaciones y tiempos de curado cuando correspondan.</p>
<p>El paso de cables debe quedar completamente estanco. Una instalación que produce perfectamente pero permite entrar agua por el techo termina siendo una mala instalación.</p>

<h2>6. Conexión eléctrica: el orden importa</h2>
<p>Consulta siempre el manual específico de tu regulador. En muchos sistemas el regulador necesita detectar primero la tensión de la batería antes de recibir energía del panel. No asumas que todos los equipos se conectan exactamente igual.</p>
<p>Como esquema conceptual, la energía sigue este recorrido:</p>
<p><strong>Panel solar → regulador MPPT/PWM → batería auxiliar → consumos de 12 V e inversor, si existe.</strong></p>
<p>Las protecciones deben colocarse y dimensionarse según el sistema. Especialmente cerca de la batería, un cortocircuito puede entregar corrientes muy elevadas, por lo que no conviene improvisar fusibles ni secciones de cable.</p>

<h2>7. Elegir correctamente el regulador MPPT</h2>
<p>No basta con mirar los vatios del panel. Comprueba la tensión de circuito abierto (Voc), corriente y potencia del conjunto de paneles y compáralas con los límites de entrada y salida indicados por el fabricante del regulador. Deja margen para condiciones de baja temperatura, que pueden elevar la tensión del panel.</p>
<p>Si instalas dos paneles, la conexión en serie o en paralelo cambia la tensión y la corriente que verá el regulador. Debe decidirse a partir de las especificaciones concretas de los paneles y del MPPT.</p>

<h2>8. Batería AGM/GEL o LiFePO4</h2>
<p>La batería debe elegirse junto con el resto del sistema. Las baterías LiFePO4 ofrecen una elevada capacidad utilizable y buena vida útil, pero requieren un sistema de carga compatible y un BMS adecuado. Si sustituyes una batería de plomo por litio, comprueba también cargador de red, alternador/booster y regulador solar, no solamente la placa.</p>

<h2>9. ¿Cuántos vatios de placa necesito?</h2>
<p>No existe una cifra universal. Para un cálculo inicial puedes dividir tu consumo diario en Wh entre las horas solares útiles previstas y añadir margen por pérdidas. Una instalación que funciona sobrada en agosto puede quedarse corta durante el invierno.</p>
<p>Si utilizas habitualmente nevera de compresor, portátil, televisión o inversor, calcula el consumo real antes de comprar. En instalaciones destinadas a viajar durante todo el año es preferible dimensionar pensando en la estación más desfavorable en la que realmente vayas a utilizar la autocaravana.</p>

<h2>10. Comprobaciones antes de dar la instalación por terminada</h2>
<ul>
<li>Revisa polaridad antes de conectar.</li>
<li>Comprueba que cables y terminales quedan firmemente sujetos.</li>
<li>Verifica fusibles y protecciones.</li>
<li>Comprueba que el pasacables y todas las fijaciones quedan sellados.</li>
<li>Confirma en el regulador que existe producción solar y carga de batería.</li>
<li>Tras los primeros viajes, inspecciona fijaciones, sellado y conexiones.</li>
</ul>

<h2>11. ITV y homologación en España</h2>
<p>Una placa fijada permanentemente al exterior del vehículo puede afectar a la consideración de reforma y a la documentación necesaria para ITV. La normativa y su interpretación dependen del tipo de instalación y vehículo, por lo que antes de perforar o fijar definitivamente los paneles conviene consultar la versión vigente del Manual de Reformas de Vehículos y confirmar el procedimiento con un profesional de homologaciones o con la estación ITV.</p>

<h2>Errores frecuentes que conviene evitar</h2>
<p>Comprar el panel antes de calcular consumos, instalar un regulador insuficiente, utilizar cable demasiado fino, olvidar las protecciones, colocar el panel donde recibe sombras, no preparar correctamente la superficie del techo y confiar el sellado a una capa improvisada de silicona son errores que pueden convertir una instalación sencilla en una fuente de problemas.</p>

<h2>Conclusión</h2>
<p>Una instalación solar bien dimensionada puede mantener cargada la batería auxiliar y aumentar considerablemente la autonomía de una autocaravana. El secreto no está en instalar la placa más grande posible, sino en equilibrar <strong>consumo, producción solar, regulador, batería, cableado y protecciones</strong>.</p>
<p>Planifica primero, mide dos veces antes de tocar el techo y trata la seguridad eléctrica y la estanqueidad como partes centrales de la instalación.</p>
"""

IMAGES = [
    "https://static.wixstatic.com/media/582360_aadbf98a8526419fb80b73b09feb87be~mv2.jpg/v1/fill/w_1000%2Ch_667%2Cal_c%2Cq_85%2Cusm_0.66_1.00_0.01/582360_aadbf98a8526419fb80b73b09feb87be~mv2.jpg",
    "https://kajabi-storefronts-production.kajabi-cdn.com/kajabi-storefronts-production/themes/2150570076/settings_images/ukHPcp3RK65MNeGHaPt9_DJI_0013.JPG",
]


def improve_post(apps, schema_editor):
    Post = apps.get_model("blog", "Post")
    PostImage = apps.get_model("blog", "PostImage")

    post = Post.objects.filter(slug=POST_SLUG).first()
    if not post:
        return

    post.title = "Guía de instalación solar para autocaravanas: placas, MPPT y batería"
    post.content = CONTENT
    post.meta_description = "Guía práctica para instalar placas solares en una autocaravana: cálculo de consumo, paneles, regulador MPPT, batería, cableado y seguridad."
    post.status = "PUBLISHED"
    post.save(update_fields=["title", "content", "meta_description", "status"])

    existing_urls = set(PostImage.objects.exclude(image_url__isnull=True).values_list("image_url", flat=True))
    for image_url in IMAGES:
        if image_url not in existing_urls:
            PostImage.objects.create(post=post, image_url=image_url)


class Migration(migrations.Migration):
    dependencies = [
        ("blog", "0062_cambiar_portada_campings_playa"),
    ]

    operations = [
        migrations.RunPython(improve_post, migrations.RunPython.noop),
    ]
