from django.conf.urls import url
from .views import ProfilesList, ProfileView

urlpatterns = {
    url(r'^profiles/$', ProfilesList.as_view(), name="all_profiles"),
    url(r'^profile/(?P<pk>\d+)/$', ProfileView.as_view(), name="one_profile"),
}