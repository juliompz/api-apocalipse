# Generated by Django 4.2 on 2023-04-10 18:38

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('aplicacao', '0002_sobrevivente_inventario'),
    ]

    operations = [
        migrations.AddField(
            model_name='sobrevivente',
            name='infectado',
            field=models.BooleanField(default=False),
        ),
    ]
