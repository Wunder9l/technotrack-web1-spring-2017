# coding: utf-8
from __future__ import unicode_literals
from django.contrib.contenttypes.fields import GenericRelation, GenericForeignKey
from django.contrib.contenttypes.models import ContentType
from django.db import models
from django.utils import timezone
from django.db.models.signals import post_save
from django.dispatch import receiver

from application.settings import MEDIA_ROOT
from core.models import User
from comments.models import Comment


# Create your models here.
def user_directory_path(instance, filename):
    # file will be uploaded to MEDIA_ROOT/user_<id>/<filename>
    return '{0}/user_{1}/{2}'.format(MEDIA_ROOT, instance.user.id, filename)


class Tag(models.Model):
    title = models.CharField(max_length=50)

    def __str__(self):  # __unicode__ on Python 2
        return self.title

    class Meta:
        ordering = ('title',)


class Taggable(models.Model):
    tag = models.ForeignKey(Tag, on_delete=models.CASCADE, related_name="tagged_objects")
    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE)
    object_id = models.PositiveIntegerField()
    content_object = GenericForeignKey('content_type', 'object_id')


class Like(models.Model):
    author = models.ForeignKey(User)
    date = models.DateTimeField(default=timezone.now)
    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE)
    object_id = models.PositiveIntegerField()
    content_object = GenericForeignKey('content_type', 'object_id')

    REQUIRED_FIELDS = ['author']


class PublicationMetaInfoQuerySet(models.QuerySet):
    def get_published_only_or_all_for_owner(self, user):
        if None is not user:
            qs = self.filter(models.Q(author_id=user.id) | models.Q(is_published=True))
        else:
            qs = self.filter(is_published=True)
        return qs


class PublicationMetaInfo(models.Model):
    is_published = models.BooleanField(default=True)
    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE)
    object_id = models.PositiveIntegerField()
    author = models.ForeignKey(User, related_name="author_publications")
    content_object = GenericForeignKey('content_type', 'object_id')
    creation_date = models.DateTimeField(default=timezone.now, editable=False)
    update_date = models.DateTimeField(default=timezone.now, editable=False)
    title = models.CharField(max_length=255)

    objects = PublicationMetaInfoQuerySet.as_manager()

    # publication_type = models.CharField(max_length=30)
    class Meta:
        ordering = ('-creation_date',)


class Publication(models.Model):
    author = models.ForeignKey(User)
    title = models.CharField(max_length=255)
    creation_date = models.DateTimeField(default=timezone.now, editable=False)
    update_date = models.DateTimeField(default=timezone.now, editable=False)
    tags = GenericRelation(Taggable)  # , related_name="%(class)s"
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
    brief_description = models.CharField(max_length=300)
    comments = GenericRelation(Comment, related_name="news_comments")
    tags = GenericRelation(Taggable, related_name="news_tags")
    likes = GenericRelation(Like, related_name="news_likes")
    meta_info = GenericRelation(PublicationMetaInfo, related_name="news_meta_info")

    class Meta(Publication.Meta):
        verbose_name = u'Новость'
        verbose_name_plural = u'Новости'

    def save(self, force_insert=False, force_update=False, using=None,
             update_fields=None):
        if self.meta_info.count() == 0:
            super(News, self).save(force_insert, force_update, using, update_fields)
            meta_info = PublicationMetaInfo(content_object=self, title=self.title, author=self.author)
            # meta_info = PublicationMetaInfo(content_object=self, title=self.title, publication_type="news")
            meta_info.save()
        else:
            super(News, self).save(force_insert, force_update, using, update_fields)
            meta_info = self.meta_info.all()[0]
            meta_info.update_date = self.update_date
            meta_info.title = self.title
            meta_info.save()


class Achievement(Publication):
    image = models.ImageField(upload_to=user_directory_path)
    comments = GenericRelation(Comment, related_name="achievement_comments")
    tags = GenericRelation(Taggable, related_name="achievement_tags")
    likes = GenericRelation(Like, related_name="achievement_likes")
    meta_info = GenericRelation(PublicationMetaInfo, related_name="achievement_meta_info")

    class Meta(Publication.Meta):
        verbose_name = u'Достижение'
        verbose_name_plural = u'Достижения'

    def save(self, force_insert=False, force_update=False, using=None,
             update_fields=None):
        if self.meta_info.count() == 0:
            super(Achievement, self).save(force_insert, force_update, using, update_fields)
            meta_info = PublicationMetaInfo(content_object=self, title=self.title, author=self.author)
            # meta_info = PublicationMetaInfo(content_object=self, title=self.title, publication_type="achievement")
            meta_info.save()
        else:
            super(Achievement, self).save(force_insert, force_update, using, update_fields)
            meta_info = self.meta_info.all()[0]
            meta_info.update_date = self.update_date
            meta_info.title = self.title
            meta_info.save()


@receiver(post_save, sender=[Achievement, News])
def apply_metainfo_to_publication(sender, **kwargs):
    print "SENDER:", sender
    print kwargs


@receiver(post_save, sender=Achievement)
def apply_metainfo_to_news(sender, **kwargs):
    print "SENDER:", sender
    print kwargs
