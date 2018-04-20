# -*- coding: utf-8 -*-
# Generated by Django 1.10 on 2018-04-20 18:43
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('login_app', '0004_remove_record_haters'),
    ]

    operations = [
        migrations.AddField(
            model_name='record',
            name='haters',
            field=models.ManyToManyField(related_name='hated_records', to='login_app.User'),
        ),
    ]
