# coding: utf-8
from __future__ import unicode_literals

from django.db import models
from application import settings

# Create your models here.
class Profile(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL)
    title = models.CharField(max_length=255)
    description = models.TextField()

    # rate = mode

class Publication(models.Model):
    author = models.ForeignKey(settings.AUTH_USER_MODEL)
    title = models.CharField(max_length=255)
    content = models.TextField()
    creation_date = models.DateField(auto_now_add=True)
    update_date = models.DateTimeField(auto_now=True)

class News(Publication):
    class Meta:
        verbose_name = u'Новость'
        verbose_name_plural = u'Новости'
        ordering = ('-creation_date',)

class Achievement(Publication):
    class Meta:
        verbose_name = u'Достижение'
        verbose_name_plural = u'Достижения'
        ordering = ('-creation_date',)
