from django.db import migrations

def create_example_affiliate_post(apps, schema_editor):
    Post = apps.get_model('blog', 'Post')
    User = apps.get_model('auth', 'User')
    
    # Intentamos obtener un autor (el primer superusuario o el primer usuario)
    author = User.objects.filter(is_superuser=True).first() or User.objects.first()
    
    if not author:
        return

    title = "Independencia Total: Guía de Instalación Solar para tu Autocaravana"
    content = (
        "## ¿Sueñas con no depender nunca más de un camping?\n\n"
        "La libertad real en el caravaning llega cuando puedes encender tu cafetera o cargar tu portátil en medio "
        "de la naturaleza sin miedo a quedarte sin energía. Para lograrlo, necesitas un ecosistema equilibrado "
        "de tres componentes: **Placas Solares, un Inversor de Onda Pura y una Batería de Litio**.\n\n"
        
        "### 1. El Corazón: Placas Solares Monocristalinas\n"
        "Para una autonomía real, recomendamos paneles de al menos 200W. Las placas monocristalinas son ideales "
        "porque aprovechan mejor la luz en días nublados.\n"
        "> **Recomendación Pro:** Este kit de 200W es el más valorado por su durabilidad. "
        "[Ver precio actualizado aquí](https://tu-enlace-de-afiliado.com/placas)\n\n"
        
        "### 2. La Transformación: Inversor de Onda Pura\n"
        "No cometas el error de comprar un inversor barato de onda modificada; podrías dañar la electrónica de tu móvil. "
        "Un inversor de onda pura de 2000W te permitirá usar incluso un secador de pelo o un microondas.\n"
        "> **Top Ventas:** Si buscas fiabilidad, este modelo de Victron es la referencia del mercado. "
        "[Consultar oferta en tienda](https://tu-enlace-de-afiliado.com/inversor)\n\n"
        
        "### 3. El Almacén: Baterías de Litio (LiFePO4)\n"
        "Es la mayor inversión, pero la más rentable. Una batería de litio de 100Ah rinde como una de 200Ah de las antiguas "
        "de AGM, pesa la mitad y dura 10 años más.\n"
        "> **Nuestra elección:** Relación calidad-precio imbatible en baterías inteligentes con Bluetooth. "
        "[Ver detalles técnicos](https://tu-enlace-de-afiliado.com/bateria)\n\n"
        
        "--- \n"
        "*Nota: Como expertos en caravaning, solo recomendamos productos que hemos probado. Este artículo contiene "
        "enlaces de afiliación que ayudan a mantener este blog sin coste alguno para ti.*"
    )

    Post.objects.get_or_create(
        slug="guia-instalacion-solar-autocaravanas",
        defaults={
            'author': author,
            'title': title,
            'content': content,
            'status': 'PUBLISHED',
        }
    )

class Migration(migrations.Migration):
    dependencies = [
        ('blog', '0005_comment'),
    ]
    operations = [
        migrations.RunPython(create_example_affiliate_post),
    ]