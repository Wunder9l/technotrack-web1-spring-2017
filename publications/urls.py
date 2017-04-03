from django.conf.urls import url
from .views import AchievementView, NewsView, PublicationsList, AchievementCreateView
urlpatterns = [
    url(r'^all/$', PublicationsList.as_view(), name="all"),

    url(r'^achievement/(?P<achievement_id>\d+)/$', AchievementView.as_view(), name="achievement_view"),
    url(r'^achievement/new/$', AchievementCreateView.as_view(), name="achievement_new"),

    url(r'^news/(?P<news_id>\d+)/$', NewsView.as_view(), name="news_view"),
    # url(r'^all/$', PublicationsList.as_view(), name="user_publications"),
]