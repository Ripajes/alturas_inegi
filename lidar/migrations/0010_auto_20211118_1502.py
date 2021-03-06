# Generated by Django 3.2.9 on 2021-11-18 21:02

import django.contrib.gis.db.models.fields
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('lidar', '0009_auto_20211118_1454'),
    ]

    operations = [
        migrations.AddField(
            model_name='poligonos',
            name='geom',
            field=django.contrib.gis.db.models.fields.MultiPolygonField(default=None, srid=4326),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='poligonos',
            name='original_id',
            field=models.BigIntegerField(default=None),
            preserve_default=False,
        ),
    ]
