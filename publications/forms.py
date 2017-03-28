# -*- coding: utf-8 -*-
from django import forms
from .models import Tag, AVAILABLE_PUBLICATIONS_TYPES, Publication


class SortForm(forms.Form):
    sort = forms.ChoiceField(choices=(
        ("creation_date", u"По дате создания"),
        ('title', u'По названию')
    ))
    search = forms.CharField(max_length=20, required=False)

# class TagForm(forms.Form):
#     tags = {tag_in_db.id: tag_in_db.title for tag_in_db in Tag.objects.all()}


class PublicationTypeSelector(forms.ChoiceField):
    types = forms.ChoiceField(choices=AVAILABLE_PUBLICATIONS_TYPES)


# class PublicationTypeSelector(forms.ChoiceField):
#     types = forms.ChoiceField(choices=AVAILABLE_PUBLICATIONS_TYPES)

class PublicationForm(forms.ModelForm):
    tags = forms.MultipleChoiceField(choices=list(Tag.objects.all()))
    publication_type = forms.ChoiceField(choices=AVAILABLE_PUBLICATIONS_TYPES)

    class Meta:
        model = Publication
        fields = ['title', 'content']

    def save(self, commit=True):
        pass