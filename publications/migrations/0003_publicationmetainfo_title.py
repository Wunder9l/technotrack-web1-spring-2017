# -*- coding: utf-8 -*-
# Generated by Django 1.10.5 on 2017-04-02 18:12
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('publications', '0002_auto_20170402_1659'),
    ]

    operations = [
        migrations.AddField(
            model_name='publicationmetainfo',
            name='title',
            field=models.CharField(default='My achievement', max_length=255),
            preserve_default=False,
        ),
    ]
