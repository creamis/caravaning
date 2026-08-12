from django.db import migrations


POST_SLUG = "lugares-mas-frescos-espana-verano-camper-autocaravana"


def create_frescos_verano_post(apps, schema_editor):
    Post = apps.get_model("blog", "Post")
    User = apps.get_model("auth", "User")

    author = User.objects.filter(username="miguel").first()
    if not author:
        author = User.objects.filter(is_superuser=True).first() or User.objects.first()
    if not author:
        return

    title = "Los 10 lugares más frescos de España para pasar el verano en camper, autocaravana o caravana"
    meta_description = (
        "Descubre 10 destinos frescos de España para escapar del calor en verano con tu camper, "
        "autocaravana o caravana y disfrutar de naturaleza y montaña."
    )

    content = """
<p><strong>Cuando llega el verano no todo el mundo sueña con 40 grados, playas abarrotadas y buscar sombra a cada paso.</strong> Para quienes viajamos en camper, autocaravana o caravana, el verano también puede ser la excusa perfecta para buscar bosques, montañas, ríos y pueblos donde las noches sean más agradables.</p>

<p>España tiene una enorme variedad de paisajes y, aunque el calor puede apretar en buena parte de la península, existen zonas del norte y de montaña donde el ambiente suele ser mucho más llevadero. Además, viajar sobre ruedas permite cambiar de escenario con facilidad y combinar naturaleza, gastronomía, rutas de senderismo y escapadas por carretera.</p>

<p>En este artículo de <strong>Caravaning Project</strong> hemos reunido diez destinos que merece la pena tener en el radar si tu objetivo este verano es <strong>escapar del calor sin renunciar a viajar en tu propia casa con ruedas</strong>.</p>

<h2>1. Asturias y los Picos de Europa</h2>
<p>Asturias es uno de los clásicos para quienes quieren pasar el verano lejos de las temperaturas extremas. La combinación de costa, valles verdes, bosques y montaña hace que sea fácil diseñar una ruta muy variada.</p>

<p>El entorno de los <strong>Picos de Europa</strong> es especialmente interesante para los viajeros en autocaravana y camper que disfrutan del senderismo. Lagos de Covadonga, Cangas de Onís, Cabrales, Sotres o los valles de los Picos permiten alternar excursiones de montaña con jornadas más tranquilas junto a ríos y pueblos.</p>

<p>Y si un día apetece cambiar las botas de montaña por la arena, la costa asturiana ofrece multitud de playas y pequeños pueblos marineros.</p>

<p><strong>Ideal para:</strong> naturaleza, senderismo, familias y rutas que combinan montaña y costa.</p>

<h2>2. Cantabria</h2>
<p>Cantabria es otra apuesta segura para el verano. Sus temperaturas suelen ser más suaves que las de muchas zonas del interior y el paisaje parece diseñado para viajar despacio: prados, bosques, acantilados, playas y montañas están relativamente cerca unos de otros.</p>

<p>El entorno de <strong>Liébana y los Picos de Europa</strong> ofrece numerosas posibilidades para quienes viajan en camper o autocaravana. También merece la pena recorrer localidades costeras y reservar tiempo para conocer Santander, Santillana del Mar, Comillas o San Vicente de la Barquera.</p>

<p>Para una ruta caravaning, uno de sus grandes atractivos es precisamente esa variedad. Puedes comenzar el día haciendo una ruta por la montaña y terminarlo viendo el atardecer junto al Cantábrico.</p>

<p><strong>Ideal para:</strong> playa, montaña, gastronomía y viajes en familia.</p>

<h2>3. Galicia y la costa de A Mariña Lucense</h2>
<p>Si buscas una combinación de temperaturas agradables, costa y tranquilidad, Galicia merece un puesto destacado. La zona de <strong>A Mariña Lucense</strong>, en la provincia de Lugo, ofrece playas, acantilados, pueblos marineros y espacios naturales perfectos para una ruta de verano.</p>

<p>Foz, Viveiro, Ribadeo y el entorno de la famosa <strong>Playa de las Catedrales</strong> permiten organizar una ruta con muchas paradas. También puedes adentrarte hacia el interior y descubrir bosques y pequeños pueblos donde el ritmo cambia por completo.</p>

<p>La gastronomía es otro motivo de peso. Después de una jornada de carretera, pocas cosas encajan mejor que sentarse a disfrutar de pescado, marisco o una buena comida gallega.</p>

<p><strong>Ideal para:</strong> costa, gastronomía, naturaleza y viajes tranquilos.</p>

<h2>4. País Vasco y la costa de Gipuzkoa</h2>
<p>El País Vasco ofrece otra alternativa para huir del calor. La costa de Gipuzkoa combina acantilados, pequeñas playas, pueblos pesqueros y montes verdes, mientras que el interior permite descubrir zonas rurales y rutas de senderismo.</p>

<p>Una ruta puede pasar por <strong>Zarautz, Getaria, Zumaia, Deba y Hondarribia</strong>, dejando tiempo para desviarse hacia espacios naturales y miradores. La proximidad entre costa y montaña permite cambiar de plan rápidamente si el día viene caluroso.</p>

<p>Además, es un destino especialmente atractivo para los amantes de la gastronomía. Una ruta en camper por Euskadi puede convertirse fácilmente en una pequeña expedición gastronómica.</p>

<p><strong>Ideal para:</strong> costa, pueblos, gastronomía y escapadas de pocos días.</p>

<h2>5. Pirineo aragonés</h2>
<p>Si lo que quieres es sustituir la playa por montañas, el <strong>Pirineo aragonés</strong> debería estar entre tus primeras opciones. La provincia de Huesca concentra algunos de los paisajes de montaña más espectaculares de España.</p>

<p>El Parque Nacional de Ordesa y Monte Perdido, el valle de Benasque, Aínsa y el entorno de los valles pirenaicos ofrecen numerosas rutas y excursiones. A mayor altitud, las temperaturas pueden resultar mucho más agradables que en las grandes ciudades del interior.</p>

<p>Para viajar en autocaravana conviene planificar bien los accesos, áreas de estacionamiento y lugares donde está permitido pernoctar. La montaña recompensa la planificación y castiga bastante la improvisación.</p>

<p><strong>Ideal para:</strong> senderismo, montaña, fotografía y viajes activos.</p>

<h2>6. Pirineo catalán</h2>
<p>El Pirineo catalán es otra gran escapada para los meses de verano. La zona de <strong>Vall de Boí, Val d'Aran y el Parque Nacional de Aigüestortes i Estany de Sant Maurici</strong> reúne lagos, bosques, pueblos de montaña y rutas para prácticamente todos los niveles.</p>

<p>La altitud es uno de sus grandes aliados frente al calor. Puedes instalar tu base en un camping o área autorizada y realizar excursiones durante el día para después regresar a un entorno mucho más fresco que el de muchas zonas costeras o del interior.</p>

<p>El Valle de Arán, además, tiene una personalidad propia y una gastronomía que merece una ruta por sí sola.</p>

<p><strong>Ideal para:</strong> montaña, senderismo, familias y amantes de los paisajes alpinos.</p>

<h2>7. Navarra y la Selva de Irati</h2>
<p>La <strong>Selva de Irati</strong> es uno de esos lugares donde el verano parece bajar el volumen. Sus grandes masas forestales, ríos y caminos convierten la zona en una excelente opción para buscar sombra y naturaleza.</p>

<p>El norte de Navarra permite combinar Irati con pueblos como Ochagavía y Orbaitzeta, además de otras zonas de montaña. Es un destino perfecto para quienes prefieren un viaje tranquilo, con caminatas, picnic y carreteras secundarias.</p>

<p>Si viajas con niños, los bosques también ofrecen una alternativa estupenda a pasar todo el día en la playa.</p>

<p><strong>Ideal para:</strong> bosques, tranquilidad, familias y senderismo.</p>

<h2>8. Sierra de Gredos</h2>
<p>No hace falta viajar hasta el extremo norte de España para encontrar zonas más frescas. La <strong>Sierra de Gredos</strong>, en el sistema Central, ofrece altitud, naturaleza y pueblos de montaña a poca distancia de Madrid y otras ciudades del centro peninsular.</p>

<p>El valle del Tiétar, Hoyos del Espino y el entorno de la plataforma de Gredos son algunos de los puntos que pueden formar parte de una ruta. Las noches en zonas elevadas pueden ser especialmente agradables cuando en las ciudades el calor sigue presente.</p>

<p>Es una opción interesante para una escapada de fin de semana o para comenzar una ruta más larga por Castilla y León.</p>

<p><strong>Ideal para:</strong> escapadas cortas, montaña y viajeros del centro de España.</p>

<h2>9. Sierra de Urbión y Laguna Negra</h2>
<p>La provincia de Soria es una de esas joyas que muchos viajeros pasan por alto. El entorno de <strong>Vinuesa, la Laguna Negra y la Sierra de Urbión</strong> ofrece bosques de pino, rutas de montaña y un ambiente muy diferente al de las zonas más calurosas de la meseta.</p>

<p>Es un destino especialmente atractivo para quienes buscan tranquilidad y quieren pasar varios días rodeados de naturaleza. Además, la zona permite combinar la ruta con visitas a pueblos y gastronomía local.</p>

<p><strong>Ideal para:</strong> tranquilidad, bosques, senderismo y desconexión.</p>

<h2>10. Valle de Arán</h2>
<p>Cerramos la lista con uno de los destinos pirenaicos más completos. El <strong>Valle de Arán</strong> ofrece pueblos de montaña, ríos, bosques, rutas y una gran cantidad de actividades al aire libre durante el verano.</p>

<p>Vielha puede servir como punto de partida para descubrir el valle, aunque merece la pena recorrer también pueblos más pequeños como Arties, Salardú o Bagergue. Las carreteras y paisajes hacen que el propio desplazamiento sea parte del viaje.</p>

<p>Para los aficionados al caravaning, es un destino que invita a quedarse varios días en lugar de hacer una visita rápida.</p>

<p><strong>Ideal para:</strong> montaña, rutas, pueblos y vacaciones activas.</p>

<h2>¿Qué hace que un destino sea realmente fresco?</h2>
<p>Cuando viajamos en camper, autocaravana o caravana, la temperatura no depende únicamente del lugar. <strong>La altitud, la orientación, la vegetación y las temperaturas nocturnas</strong> pueden cambiar muchísimo la experiencia.</p>

<p>Una zona situada a cierta altura puede resultar muy agradable durante el día y necesitar una chaqueta por la noche. En cambio, algunos destinos costeros pueden tener temperaturas moderadas pero una humedad elevada que hace que la sensación térmica sea diferente.</p>

<p>Por eso, antes de elegir destino, conviene consultar la previsión meteorológica para los días concretos del viaje y tener siempre un plan alternativo.</p>

<h2>Consejos para viajar en camper o autocaravana durante una ola de calor</h2>
<ul>
<li><strong>Busca zonas con sombra</strong>, especialmente si vas a permanecer varias horas estacionado.</li>
<li><strong>Prioriza campings y áreas autorizadas</strong> que dispongan de servicios adecuados para tu vehículo.</li>
<li><strong>Ventila a primera hora y por la noche</strong>, cuando la temperatura exterior sea más baja.</li>
<li><strong>Lleva agua suficiente</strong> y no dependas de encontrar un punto de suministro inmediatamente.</li>
<li><strong>Planifica las rutas de senderismo</strong> evitando las horas centrales del día.</li>
<li><strong>Revisa la normativa local de estacionamiento y pernocta</strong> antes de instalarte.</li>
<li><strong>No fuerces el aire acondicionado ni otros equipos</strong> si tu instalación eléctrica no está preparada para ello.</li>
<li><strong>Consulta el riesgo de incendios</strong> en las zonas rurales y respeta todas las restricciones vigentes.</li>
</ul>

<h2>¿Camper, autocaravana o caravana?</h2>
<p>Los tres formatos permiten disfrutar de estos destinos, aunque cada uno tiene sus ventajas. La <strong>camper</strong> suele resultar especialmente cómoda para moverse por carreteras estrechas y hacer rutas con muchas paradas. La <strong>autocaravana</strong> ofrece más espacio y autonomía para viajes largos, mientras que la <strong>caravana</strong> puede ser una opción fantástica si quieres instalarte varios días en un camping y utilizar el coche para recorrer los alrededores.</p>

<p>En todos los casos, la clave está en adaptar la ruta al vehículo y no al revés. Un destino maravilloso deja de ser tan maravilloso cuando intentamos meter una autocaravana de siete metros por una calle medieval que parece diseñada para una bicicleta.</p>

<h2>La mejor forma de escapar del calor</h2>
<p>Una de las grandes ventajas del caravaning es precisamente la libertad de cambiar de escenario. Si la previsión anuncia temperaturas muy altas en la costa, puedes subir a la montaña. Si una zona del norte viene acompañada de lluvia, puedes modificar la ruta y buscar otro destino.</p>

<p>Asturias, Cantabria, Galicia, el Pirineo, Navarra, Gredos o las sierras del interior ofrecen alternativas para todos los estilos de viaje. Lo importante es planificar con sentido común, respetar los espacios naturales y utilizar siempre lugares donde esté permitido estacionar y pernoctar.</p>

<p><strong>Así que este verano, si el termómetro empieza a echar humo, no hace falta quedarse encerrado en casa.</strong> Carga agua, prepara la nevera, revisa la ruta y deja que tu casa con ruedas te lleve hacia temperaturas más agradables.</p>

<p><strong>¿Cuál es tu destino favorito para escapar del calor en camper, autocaravana o caravana?</strong> Déjanos tu recomendación y ayúdanos a ampliar esta lista.</p>
""".strip()

    Post.objects.update_or_create(
        slug=POST_SLUG,
        defaults={
            "author": author,
            "title": title,
            "content": content,
            "meta_description": meta_description,
            "status": "PUBLISHED",
        },
    )


def remove_frescos_verano_post(apps, schema_editor):
    Post = apps.get_model("blog", "Post")
    Post.objects.filter(slug=POST_SLUG).delete()


class Migration(migrations.Migration):
    dependencies = [
        ("blog", "0010_seed_benimar_s363_post"),
    ]

    operations = [
        migrations.RunPython(create_frescos_verano_post, remove_frescos_verano_post),
    ]
