# -*- coding: utf-8 -*-
from django import forms
from django.core.validators import RegexValidator

from .publication_type_resolver import AVAILABLE_PUBLICATIONS_TYPES

tagsFieldValidator = RegexValidator(regex=r'^[a-z,]+$',
                                    message=u"Тэги должны быть записаны через запятую, допускаются только строчные"
                                            u" латинские буквы",
                                    code='invalid_tags_field')


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
    #
    # def __init__(self, *args, ** kwargs):
    #     super(SortForm, self).__init__(*args, **kwargs)
    #     print "IN FORM: ", [x[0] for x in AVAILABLE_PUBLICATIONS_TYPES]
    #     self.initial['publication_type'] = ['news']


class PublicationTypeSelector(forms.ChoiceField):
    types = forms.ChoiceField(choices=AVAILABLE_PUBLICATIONS_TYPES)


class PublicationTemplateForm(forms.Form):
    title = forms.CharField(max_length=150, label=u'Название')
    brief_description = forms.CharField(required=False, label=u'Краткое описание', max_length=300)
    content = forms.Textarea()  # label=u'Содержание'
    image = forms.ImageField()
    tags = forms.CharField(max_length=150, required=False, label=u'Тэги', validators=[tagsFieldValidator])
    # publication_type = forms.ChoiceField(choices=AVAILABLE_PUBLICATIONS_TYPES)

    # def save(self, commit=True):
    #     # Handle tags field
    #     pass


class AchievementForm(PublicationTemplateForm):

    def __init__(self, *args, **kwargs):
        print args
        print kwargs
        return super(AchievementForm, self).__init__(*args, **kwargs)

