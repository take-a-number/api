# -*- coding: utf-8 -*-
# Generated by Django 1.11.4 on 2018-11-26 04:15
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('take_a_number', '0004_remove_officehourssession_instructor_code'),
    ]

    operations = [
        migrations.AddField(
            model_name='officehourssession',
            name='instructor_code',
            field=models.SlugField(default='', max_length=6),
        ),
        migrations.AddField(
            model_name='officehourssession',
            name='student_code',
            field=models.SlugField(default='', max_length=6),
        ),
    ]
