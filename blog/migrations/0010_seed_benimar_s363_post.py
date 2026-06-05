from django.db import migrations


POST_SLUG = "benimar-sport-s363-2026-autocaravana-vacaciones"

IMAGE_URLS = [
    "https://www.benimar.es/wp-content/uploads/Sport-2026__DSC6084-Editar_S363_T26.jpg",
    "https://www.benimar.es/wp-content/uploads/Sport-2026__DSC6072-Editar_S363_T26.jpg",
    "https://www.benimar.es/wp-content/uploads/Sport-2026__DSC6057-Editar_S363_T26.jpg",
    "https://www.benimar.es/wp-content/uploads/Sport-2026__DSC6092_S363_T26.jpg",
    "https://www.benimar.es/wp-content/uploads/Sport-2026__DSC6097_S363_T26.jpg",
    "https://www.benimar.es/wp-content/uploads/Sport-2026__DSC6099_S363_T26.jpg",
    "https://www.benimar.es/wp-content/uploads/Sport-2026__DSC6105_S363_T26.jpg",
    "https://www.benimar.es/wp-content/uploads/Sport-2026__81A4558_S363_T26.jpg",
    "https://www.benimar.es/wp-content/uploads/Sport-2026__81A4570_S363_T26-1.jpg",
    "https://www.benimar.es/wp-content/uploads/Sport-2026__81A4596_S363_T26-1.jpg",
    "https://www.benimar.es/wp-content/uploads/Sport-2026__81A4602_S363_T26-1.jpg",
    "https://www.benimar.es/wp-content/uploads/Sport-2026__81A4618_S363_T26-1.jpg",
]


def create_benimar_s363_post(apps, schema_editor):
    Post = apps.get_model("blog", "Post")
    PostImage = apps.get_model("blog", "PostImage")
    User = apps.get_model("auth", "User")

    author = User.objects.filter(is_superuser=True).first() or User.objects.first()
    if not author:
        return

    title = "Benimar Sport S363 2026: una autocaravana familiar para estas vacaciones"
    meta_description = (
        "Benimar Sport S363 2026: autocaravana capuchina de 5 plazas con gran garaje, "
        "cama capuchina, camas gemelas y cocina en L."
    )
    content = """
<p><strong>La Benimar Sport S363 2026</strong> es una autocaravana capuchina pensada para viajar en familia o con amigos sin renunciar a camas reales, almacenamiento amplio y una distribucion muy practica para vacaciones largas.</p>

<p>Este modelo forma parte de la gama Sport 2026 de Benimar y se apoya en chasis Ford Euro 6 con motor 2.0 l de 130 CV y cambio manual de 6 velocidades. Su planteamiento es claro: cinco plazas homologadas, cinco plazas para comer y cinco plazas para dormir, con una longitud de 743 cm, anchura de 230 cm y altura de 308 cm.</p>

<h2>Por que encaja tan bien para vacaciones</h2>
<p>La S363 destaca por combinar una cama capuchina de gran tamano con camas gemelas traseras transformables en una cama doble. Esa configuracion permite que una familia pueda viajar sin montar y desmontar el salon cada noche, algo que se agradece especialmente en rutas de verano, escapadas largas o viajes con ninos.</p>

<ul>
  <li><strong>Plazas:</strong> 5 en circulacion, 5 para comer y 5 para dormir.</li>
  <li><strong>Longitud:</strong> 743 cm.</li>
  <li><strong>Garaje:</strong> amplio, con dos portones y acceso desde el interior.</li>
  <li><strong>Cocina:</strong> distribucion en L con frigorifico de compresor de 150 l.</li>
  <li><strong>Bano:</strong> ducha independiente y espejo retroiluminado.</li>
  <li><strong>Dormitorio:</strong> camas gemelas transformables en cama doble de 170 x 210 cm.</li>
  <li><strong>Cama capuchina:</strong> 155 x 203 cm segun ficha tecnica.</li>
</ul>

<h2>Descripcion del vehiculo</h2>
<p>Exteriormente, la Benimar Sport S363 mantiene el formato capuchino clasico: mas altura, mas cama disponible y una sensacion de vehiculo familiar desde el primer vistazo. La carroceria prioriza el volumen util y el acceso al garaje, una ventaja para llevar mesas, sillas, calzos, equipaje, material deportivo o accesorios de playa.</p>

<p>En el interior, el salon con mesa extensible busca ser usable durante el dia sin que la cama capuchina interfiera. La cocina en L es uno de sus puntos mas interesantes para viajes reales, porque separa mejor la zona de trabajo y permite cocinar con mas comodidad que en distribuciones lineales compactas. El frigorifico de 150 l tambien apunta a escapadas de varios dias, no solo a fines de semana.</p>

<p>La zona trasera apuesta por camas gemelas, una solucion muy comoda para adultos y que, al transformarse en una cama doble grande, da flexibilidad segun el tipo de viaje. A esto se suma una puerta de separacion entre dormitorio y salon, util para ganar privacidad cuando se viaja con familia.</p>

<h2>Lo mejor del Benimar Sport S363 2026</h2>
<p><strong>Su punto fuerte es la vida a bordo.</strong> No es el modelo mas pequeno ni pretende serlo: mide 7,43 metros y esta pensado para quien valora espacio, almacenaje y camas permanentes. Para vacaciones de verano, rutas por costa o viajes con varias personas, esa amplitud puede marcar la diferencia.</p>

<p>Tambien resulta interesante el enfoque familiar: ISOFIX en los asientos del comedor con Pack PLUS, gran garaje, acceso interior al garaje, ducha independiente y un salon que sigue siendo util aunque alguien este descansando en la capuchina.</p>

<h2>A tener en cuenta antes de elegirla</h2>
<p>Por tamano, no es la autocaravana mas agil para cascos urbanos estrechos o parkings pequenos. Su longitud invita mas a viajar con planificacion, elegir bien las areas de pernocta y aprovechar su capacidad en ruta. A cambio, ofrece una experiencia mucho mas habitable que una camper compacta.</p>

<h2>Veredicto Caravaning Project</h2>
<p>La Benimar Sport S363 2026 tiene mucho sentido para familias que buscan una autocaravana de vacaciones con cinco plazas reales, cama capuchina, dormitorio trasero separado y garaje generoso. Es una opcion especialmente atractiva para quienes priorizan comodidad interior, almacenaje y autonomia practica frente a la maxima compacidad.</p>

<p><small>Datos e imagenes consultados en la ficha oficial de Benimar Sport S363 2026. Las caracteristicas pueden variar segun mercado, pack y configuracion. Fuente: <a href="https://www.benimar.es/sport/s363/" target="_blank" rel="noopener">Benimar S363</a>.</small></p>
""".strip()

    post, _ = Post.objects.update_or_create(
        slug=POST_SLUG,
        defaults={
            "author": author,
            "title": title,
            "content": content,
            "meta_description": meta_description,
            "status": "PUBLISHED",
        },
    )

    PostImage.objects.filter(post=post).delete()
    for image_url in IMAGE_URLS:
        PostImage.objects.create(post=post, image_url=image_url)


def remove_benimar_s363_post(apps, schema_editor):
    Post = apps.get_model("blog", "Post")
    Post.objects.filter(slug=POST_SLUG).delete()


class Migration(migrations.Migration):
    dependencies = [
        ("blog", "0009_alter_post_status"),
    ]

    operations = [
        migrations.RunPython(create_benimar_s363_post, remove_benimar_s363_post),
    ]
