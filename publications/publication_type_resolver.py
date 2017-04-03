# -*- coding: utf-8 -*-
from django.shortcuts import resolve_url

from .models import *


PUBLICATION_TYPE_TO_MODEL = {"news": News, "achievement": Achievement}
AVAILABLE_PUBLICATIONS_TYPES = (('news', "Новость"), ('achievement', "Достижение"))


def get_publication_view_url(model_or_name, id):
    if model_or_name in PUBLICATION_TYPE_TO_MODEL:
        model = PUBLICATION_TYPE_TO_MODEL[model_or_name]
    else:
        model = model_or_name
    if model == Achievement:
        return resolve_url('publications:achievement_view', achievement_id=id)
    elif model == News:
        return resolve_url('publications:news_view', news_id=id)
    else:
        return None