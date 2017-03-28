from django.contrib import admin
from .models import Publication, Tag

# Register your models here.
admin.site.register(Publication)
admin.site.register(Tag)
# admin.site.register(Achievement)