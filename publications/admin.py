from django.contrib import admin

from publications.models import PublicationMetaInfo, Achievement, News, Tag


# Register your models here.
admin.site.register(News)
admin.site.register(Achievement)
admin.site.register(Tag)
admin.site.register(PublicationMetaInfo)
# admin.site.register(Achievement)