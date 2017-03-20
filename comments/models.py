from __future__ import unicode_literals

from django.db import models
from django.utils import timezone

from application import settings
from publications.models import Publication

class Comment(models.Model):
    author = models.ForeignKey(settings.AUTH_USER_MODEL)
    publication = models.ForeignKey(Publication)
    creation_date = models.DateTimeField(default=timezone.now)
    update_date = models.DateTimeField(default=timezone.now)
    content = models.TextField()

# Create your models here.
