# -*- coding: utf-8 -*-
# Generated by Django 1.10 on 2018-04-20 15:44
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('login_app', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Record',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('artist', models.CharField(max_length=255)),
                ('album', models.CharField(max_length=255)),
                ('label', models.CharField(max_length=255)),
                ('haters', models.ManyToManyField(related_name='hated_records', to='login_app.User')),
                ('uploader', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='uploads', to='login_app.User')),
            ],
        ),
    ]
