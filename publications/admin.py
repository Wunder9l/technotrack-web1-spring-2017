from django.contrib import admin
from .models import Achievement, News, Tag

# Register your models here.
admin.site.register(News)
admin.site.register(Achievement)
admin.site.register(Tag)
# admin.site.register(Achievement)