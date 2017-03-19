# coding: utf-8
from __future__ import unicode_literals


from django.db import models
from django.utils import timezone

from core.models import User
from application import settings

# Create your models here.

class Publication(models.Model):
    author = models.ForeignKey(User)
    title = models.CharField(max_length=255)
    content = models.TextField()
    creation_date = models.DateTimeField(default=timezone.now)
    update_date = models.DateTimeField(auto_now=True)
    publication_type = models.CharField(max_length=40)
    class Meta:
        ordering = ('-creation_date',)
        # verbose_name = u'Публикация'
        # verbose_name_plural = u'Публикации'


class News(Publication):
    class Meta:
        proxy = True
        # verbose_name = u'Новость'
        # verbose_name_plural = u'Новости'

class Achievement(Publication):
    class Meta:
        proxy = True
        # verbose_name = u'Достижение'
        # verbose_name_plural = u'Достижения'
