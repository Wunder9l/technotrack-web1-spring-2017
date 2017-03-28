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

    def post_publication(self, publication_title, content, publication_type, tags):
        from publications.models import Publication
        publication = Publication(author=self, title=publication_title, content=content,
                                  publication_type=publication_type, tags=tags)
        publication.save()

    def post_comment(self, publication, content):
        from comments.models import Comment
        comment = Comment(publication=publication, author=self, content=content)
        comment.save()
