# -*- coding: utf-8 -*-
# Generated by Django 1.11.3 on 2018-05-13 21:58
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('products', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='product',
            name='product_type',
            field=models.CharField(choices=[('Top', 'Top'), ('Bottom', 'Bottom'), ('Hat', 'Hat'), ('Shoe', 'Shoe'), ('Jewelry', 'Jewelry')], max_length=13),
        ),
    ]
