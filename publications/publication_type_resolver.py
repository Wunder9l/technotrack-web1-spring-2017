# -*- coding: utf-8 -*-
from django.shortcuts import resolve_url

from .models import *

PUBLICATION_TYPE_TO_MODEL = {"news": News, "achievement": Achievement}
MODEL_TO_PUBLICATION_TYPE = {value: key for key, value in PUBLICATION_TYPE_TO_MODEL.iteritems()}
AVAILABLE_PUBLICATIONS_TYPES = (('news', "Новость"), ('achievement', "Достижение"))
MODEL_TO_CONTENT_TYPE = {key: ContentType.objects.get_for_model(key)
                         for key in PUBLICATION_TYPE_TO_MODEL.values()}
PUBLICATION_TYPE_TO_CONTENT_TYPE = {MODEL_TO_PUBLICATION_TYPE[key]: value
                                    for key, value in MODEL_TO_CONTENT_TYPE.iteritems()}
MODEL_TO_PUBLICATION_VIEW_URL = {Achievement: 'publications:achievement_view',
                                 News: 'publications:news_view'}
MODEL_TO_PUBLICATION_EDIT_URL = {Achievement: 'publications:achievement_edit',
                                 News: 'publications:news_edit'}


def get_publication_view_url(model_or_name, publication_id):
    if model_or_name in PUBLICATION_TYPE_TO_MODEL:
        model = PUBLICATION_TYPE_TO_MODEL[model_or_name]
    else:
        model = model_or_name
    return resolve_url(MODEL_TO_PUBLICATION_VIEW_URL[model], publication_id)


def get_publication_edit_url(model_or_name, publication_id):
    if model_or_name in PUBLICATION_TYPE_TO_MODEL:
        model = PUBLICATION_TYPE_TO_MODEL[model_or_name]
    else:
        model = model_or_name
    return resolve_url(MODEL_TO_PUBLICATION_EDIT_URL[model], publication_id)
