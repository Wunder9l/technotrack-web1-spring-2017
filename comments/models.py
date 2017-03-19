from __future__ import unicode_literals

from django.db import models
from application import settings
from publications.models import Publication

class Comment(models.Model):
    author = models.ForeignKey(settings.AUTH_USER_MODEL)
    publication = models.ForeignKey(Publication)
    creation_date = models.DateField(auto_now_add=True)
    update_date = models.DateTimeField(auto_now=True)
    content = models.TextField()

# Create your models here.
