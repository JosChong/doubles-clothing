# -*- coding: utf-8 -*-
# Generated by Django 1.11.3 on 2018-05-13 22:01
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('products', '0002_auto_20180513_2158'),
    ]

    operations = [
        migrations.AlterField(
            model_name='product',
            name='product_type',
            field=models.CharField(choices=[('Top', 'Top'), ('Bottom', 'Bottom'), ('Hat', 'Hat'), ('Shoe', 'Shoe'), ('Accessory', 'Accessory')], max_length=13),
        ),
    ]
