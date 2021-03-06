# -*- coding: utf-8 -*-
# Generated by Django 1.11.4 on 2018-11-06 04:20
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Class',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('instr_name', models.CharField(blank='', max_length=200)),
                ('instr_email', models.EmailField(blank='', max_length=200)),
                ('school', models.CharField(blank='', max_length=200)),
                ('course_name', models.SlugField(blank='', max_length=200)),
                ('keywords', models.CharField(blank='', max_length=500)),
            ],
        ),
    ]
