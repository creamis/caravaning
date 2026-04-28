from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0005_comment'),
    ]

    operations = [
        migrations.AddField(
            model_name='post',
            name='meta_description',
            field=models.CharField(blank=True, help_text='Descripción para buscadores (Google). Máx 160 caracteres.', max_length=160, verbose_name='Meta descripción'),
        ),
    ]