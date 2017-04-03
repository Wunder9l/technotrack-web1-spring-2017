from __future__ import unicode_literals

from django.db import models
from django.contrib.auth.models import AbstractUser


# Create your models here.
class User(AbstractUser):
    full_name = None

    def __init__(self, *args, **kwargs):
        super(User, self).__init__(*args, **kwargs)
        self.full_name = "%s %s (%s)" % (self.first_name, self.last_name, self.username)

    # name = models.CharField(255)
    # avatar = models.ImageField(upload_to='avatars', blank=True, null=True)

    # def post_publication(self, publication_title, content, publication_type, tags):
    #     from publications.models import Publication
    #     publication = Publication(author=self, title=publication_title, content=content,
    #                               publication_type=publication_type, tags=tags)
    #     publication.save()

    def post_achievement(self, achievement_title, tags):
        '''
        :param achievement_title: Title of posted achievement
        :param tags: list of Tag objects
        :return: nothing
        '''
        from publications.models import Achievement
        news = Achievement(author=self, title=achievement_title, tags=tags)
        news.save()

    def post_news(self, news_title, tags):
        '''
        :param news_title: Title of posted news
        :param tags: list of Tag objects
        :return: nothing
        '''
        from publications.models import News
        news = News(author=self, title=news_title, tags=tags)
        news.save()

    def post_comment(self, publication, content):
        from comments.models import Comment
        comment = Comment(publication=publication, author=self, content=content)
        comment.save()
