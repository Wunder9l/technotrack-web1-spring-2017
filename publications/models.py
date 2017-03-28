# coding: utf-8
from __future__ import unicode_literals

from django.db import models
from django.utils import timezone

from core.models import User
from application import settings

# Create your models here.
AVAILABLE_PUBLICATIONS_TYPES = {'news': "Новость", 'achievement': "Достижение"}


class Publication(models.Model):
    author = models.ForeignKey(User)
    title = models.CharField(max_length=255)
    content = models.TextField()
    creation_date = models.DateTimeField(default=timezone.now)
    update_date = models.DateTimeField(default=timezone.now)
    publication_type = models.CharField(max_length=40)

    # tags = models.ManyToManyField(Tag)

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


class Tag(models.Model):
    title = models.CharField(max_length=50)
    publications = models.ManyToManyField(Publication)

    # REQUIRED_FIELDS = ['title']
    def __str__(self):  # __unicode__ on Python 2
        return self.title

    class Meta:
        ordering = ('title',)


class Like(models.Model):
    author = models.ForeignKey(User)
    liked_object = models.ForeignKey(Publication)
    date = models.DateTimeField(default=timezone.now)
    REQUIRED_FIELDS = ['author']
