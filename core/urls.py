from django.conf.urls import url
from core.views import UserView, UsersList


urlpatterns = [
    url(r'^s/$', UsersList.as_view(), name="all_users"),
    url(r'^/(?P<user_id>\d+)/$', UserView.as_view(), name="one_user"),
]
