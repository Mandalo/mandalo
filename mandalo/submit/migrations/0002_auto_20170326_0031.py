# -*- coding: utf-8 -*-
# Generated by Django 1.10.6 on 2017-03-26 00:31
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('submit', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='assignment',
            name='due_date',
            field=models.DateField(verbose_name='Due Date'),
        ),
    ]