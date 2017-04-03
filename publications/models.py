# coding: utf-8
from __future__ import unicode_literals

from django.contrib.contenttypes.fields import GenericRelation, GenericForeignKey
from django.contrib.contenttypes.models import ContentType
from django.db import models
from django.utils import timezone

from core.models import User
from comments.models import Comment

# Create your models here.


class Tag(models.Model):
    title = models.CharField(max_length=50)
    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE)
    object_id = models.PositiveIntegerField()
    content_object = GenericForeignKey('content_type', 'object_id')

    def __str__(self):  # __unicode__ on Python 2
        return self.title

    class Meta:
        ordering = ('title',)


class Like(models.Model):
    author = models.ForeignKey(User)
    date = models.DateTimeField(default=timezone.now)
    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE)
    object_id = models.PositiveIntegerField()
    content_object = GenericForeignKey('content_type', 'object_id')

    REQUIRED_FIELDS = ['author']


class PublicationMetaInfo(models.Model):
    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE)
    object_id = models.PositiveIntegerField()
    content_object = GenericForeignKey('content_type', 'object_id')
    creation_date = models.DateTimeField(default=timezone.now)
    update_date = models.DateTimeField(default=timezone.now)
    title = models.CharField(max_length=255)
    publication_type = models.CharField(max_length=30)


class Publication(models.Model):
    author = models.ForeignKey(User)
    title = models.CharField(max_length=255)
    creation_date = models.DateTimeField(default=timezone.now)
    update_date = models.DateTimeField(default=timezone.now)
    brief_description = models.CharField(max_length=300)
    tags = GenericRelation(Tag)  # , related_name="%(class)s"
    comments = GenericRelation(Comment)
    likes = GenericRelation(Like)
    meta_info = GenericRelation(PublicationMetaInfo)
    REQUIRED_FIELDS = ['author', 'title', ]

    class Meta:
        abstract = True
        ordering = ('-creation_date',)

    def save(self, force_insert=False, force_update=False, using=None,
             update_fields=None):
        super(Publication, self).save(force_insert, force_update, using, update_fields)


class News(Publication):
    comments = GenericRelation(Comment, related_name="news_comments")
    tags = GenericRelation(Tag, related_name="news_tags")
    likes = GenericRelation(Like, related_name="news_likes")
    meta_info = GenericRelation(PublicationMetaInfo, related_name="news_meta_info")

    class Meta(Publication.Meta):
        verbose_name = u'Новость'
        verbose_name_plural = u'Новости'

    def save(self, force_insert=False, force_update=False, using=None,
             update_fields=None):
        if self.meta_info.count() == 0:
            super(News, self).save(force_insert, force_update, using, update_fields)
            meta_info = PublicationMetaInfo(content_object=self, title=self.title, publication_type="news")
            meta_info.save()
        else:
            super(News, self).save(force_insert, force_update, using, update_fields)
            meta_info = self.meta_info.all()[0]
            meta_info.update_date = self.update_date
            meta_info.title = self.title
            meta_info.save()


class Achievement(Publication):
    comments = GenericRelation(Comment, related_name="achievement_comments")
    tags = GenericRelation(Tag, related_name="achievement_tags")
    likes = GenericRelation(Like, related_name="achievement_likes")
    meta_info = GenericRelation(PublicationMetaInfo, related_name="achievement_meta_info")

    class Meta(Publication.Meta):
        verbose_name = u'Достижение'
        verbose_name_plural = u'Достижения'

    def save(self, force_insert=False, force_update=False, using=None,
             update_fields=None):
        if self.meta_info.count() == 0:
            super(Achievement, self).save(force_insert, force_update, using, update_fields)
            meta_info = PublicationMetaInfo(content_object=self, title=self.title, publication_type="achievement")
            meta_info.save()
        else:
            super(Achievement, self).save(force_insert, force_update, using, update_fields)
            meta_info = self.meta_info.all()[0]
            meta_info.update_date = self.update_date
            meta_info.title = self.title
            meta_info.save()
