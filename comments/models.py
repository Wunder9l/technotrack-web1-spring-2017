# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models
from django.utils import timezone
from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType
from application import settings


class Comment(models.Model):
    reply_to = models.ForeignKey('self')
    author = models.ForeignKey(settings.AUTH_USER_MODEL)
    creation_date = models.DateTimeField(default=timezone.now)
    update_date = models.DateTimeField(default=timezone.now)
    content = models.TextField(verbose_name=u'Содержание')
    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE)
    object_id = models.PositiveIntegerField()
    content_object = GenericForeignKey('content_type', 'object_id')

    class Meta:
        ordering = ('-creation_date',)

# Create your models here.
