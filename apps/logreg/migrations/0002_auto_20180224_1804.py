# -*- coding: utf-8 -*-
# Generated by Django 1.11.10 on 2018-02-24 23:04
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('logreg', '0001_initial'),
    ]

    operations = [
        migrations.RenameField(
            model_name='user',
            old_name='first_name',
            new_name='first',
        ),
        migrations.RenameField(
            model_name='user',
            old_name='last_name',
            new_name='last',
        ),
    ]