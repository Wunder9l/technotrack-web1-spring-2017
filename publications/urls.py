from django.conf.urls import url
from .views import PublicationView, PublicationsList
urlpatterns = [
    url(r'^all/$', PublicationsList.as_view(), name="all_publications"),
    url(r'^(?P<publication_id>\d+)/$', PublicationView.as_view(), name="one_publications"),
    # url(r'^all/$', PublicationsList.as_view(), name="user_publications"),
]