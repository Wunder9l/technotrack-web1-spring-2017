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