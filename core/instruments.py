# -*- coding: utf-8 -*-
from django.core.cache import caches

cache = caches['default']


def get_cached_or_qs(cache_key, qs, time_to_live):
    value = cache.get(cache_key)
    if None is value:
        value = qs()
        cache.set(cache_key, value, time_to_live)
    return value
