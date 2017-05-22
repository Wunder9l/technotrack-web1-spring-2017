from django.contrib.auth.views import login, logout
from core.views import UserView, UsersList, MainPage, UserRegistrationView
from django.conf.urls import include, url

urlpatterns = [
    url(r'^$', MainPage.as_view(), name="main_page"),
    url(r'^users/$', UsersList.as_view(), name="all_users"),
    url(r'^user/(?P<user_id>\d+)/$', UserView.as_view(), name="one_user"),
    url(r'^login/$', login, {'template_name': 'core/login.html'}, name="login"),
    url(r'^logout/$', logout, name="logout"),
    url(r'^registration/$', UserRegistrationView.as_view(), name="registration"),
]
