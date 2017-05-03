from django import template

from publications.publication_type_resolver import get_publication_view_url, get_publication_edit_url

register = template.Library()


@register.simple_tag
def publication_view_url(publication_meta_info):
    return get_publication_view_url(type(publication_meta_info.content_object),
                                    publication_meta_info.object_id)


@register.simple_tag
def publication_edit_url(publication_meta_info):
    return get_publication_edit_url(type(publication_meta_info.content_object),
                                    publication_meta_info.object_id)
