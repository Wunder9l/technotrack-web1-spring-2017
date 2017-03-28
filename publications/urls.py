from django.conf.urls import url
from .views import PublicationView, PublicationsList, PublicationCreateView
urlpatterns = [
    url(r'^all/$', PublicationsList.as_view(), name="all"),
    url(r'^(?P<publication_id>\d+)/$', PublicationView.as_view(), name="view"),
    url(r'^new/$', PublicationCreateView.as_view(), name="new"),
    # url(r'^all/$', PublicationsList.as_view(), name="user_publications"),
]