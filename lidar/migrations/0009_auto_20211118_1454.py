# Generated by Django 3.2.9 on 2021-11-18 20:54

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('lidar', '0008_poligonos'),
    ]

    operations = [
        migrations.AddField(
            model_name='poligonos',
            name='h_max',
            field=models.DecimalField(decimal_places=2, default=0, max_digits=7),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='poligonos',
            name='h_mean',
            field=models.DecimalField(decimal_places=2, default=0, max_digits=7),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='poligonos',
            name='h_min',
            field=models.DecimalField(decimal_places=2, default=0, max_digits=7),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='poligonos',
            name='h_range',
            field=models.DecimalField(decimal_places=2, default=0, max_digits=7),
            preserve_default=False,
        ),
    ]
