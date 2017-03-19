"""application url configuration

the `urlpatterns` list routes urls to views. for more information please see:
    https://docs.djangoproject.com/en/1.10/topics/http/urls/
examples:
function views
    1. add an import:  from my_app import views
    2. add a url to urlpatterns:  url(r'^$', views.home, name='home')
class-based views
    1. add an import:  from other_app.views import home
    2. add a url to urlpatterns:  url(r'^$', home.as_view(), name='home')
including another urlconf
    1. import the include() function: from django.conf.urls import url, include
    2. add a url to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import url, include
from django.contrib import admin
from core.views import MainPage
# from core.models import
urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^$', MainPage.as_view(), name="main_page"),
    url(r'^user', include('core.urls', namespace="users")),
    url(r'^publications/', include('publications.urls', namespace="publications")),
]
