# -*- coding: utf-8 -*-
from django import forms
from django.contrib.contenttypes.models import ContentType
from django.core.validators import RegexValidator

from publications.models import Achievement, Tag, Taggable
from .publication_type_resolver import AVAILABLE_PUBLICATIONS_TYPES

tags_field_validator = RegexValidator(regex=ur'^[а-яa-z0-9,_]+$',
                                      message=u"Тэги должны быть записаны через запятую, допускаются только строчные "
                                              u"русские и латинские буквы, цифры и знаки подчеркивания",
                                      code='invalid_tags_field')


def set_tags_for_instance(instance, tags_string):
    tags = tags_string.split(u",")
    found_tags = Tag.objects.filter(title__in=tags)
    for tag in found_tags:
        if tag.tagged_objects.filter(content_type__pk=ContentType.objects.get_for_model(instance).id,
                                     object_id=instance.id).count() is 0:
            tagged_object = Taggable(tag=tag, content_object=instance)
            tagged_object.save()
        tags.remove(tag.title)
    for tag_title in tags:
        tag = Tag(title=tag_title)
        tag.save()
        tagged_object = Taggable(tag=tag, content_object=instance)
        tagged_object.save()


class SortForm(forms.Form):
    sort = forms.ChoiceField(choices=(
        ("creation_date", u"По дате создания"),
        ('title', u'По названию')
    ), widget=forms.Select)
    publication_type = forms.MultipleChoiceField(choices=AVAILABLE_PUBLICATIONS_TYPES,
                                                 label=u"Типы публикаций",
                                                 widget=forms.widgets.CheckboxSelectMultiple,
                                                 initial=[x[0] for x in AVAILABLE_PUBLICATIONS_TYPES],
                                                 required=False
                                                 )
    search = forms.CharField(max_length=20, required=False)


class PublicationTemplateForm(forms.ModelForm):
    title = forms.CharField(max_length=150, label=u'Название')
    brief_description = forms.CharField(required=False, label=u'Краткое описание', max_length=300)
    content = forms.CharField(widget=forms.Textarea, label=u'Содержание')
    # image = forms.ImageField()
    tags = forms.CharField(max_length=150, required=False, label=u'Тэги', validators=[tags_field_validator])

    # publication_type = forms.ChoiceField(choices=AVAILABLE_PUBLICATIONS_TYPES)


class AchievementForm(PublicationTemplateForm):
    def save(self, commit=True):
        instance = super(AchievementForm, self).save(self)
        # instance.author = get_user
        tags = self.cleaned_data["tags"]
        set_tags_for_instance(instance, tags)

    class Meta:
        model = Achievement
        fields = ["title", 'brief_description', ]
