from django.conf.urls import url
from django.contrib.auth.decorators import login_required

from publications.views_news import CreateNewsView, EditNewsView, EditNewsViewInline
from .views import AchievementView, PublicationsList, CreateAchievementView, EditAchievementView, NewsView

urlpatterns = [
    url(r'^all/$', PublicationsList.as_view(), name="all"),

    url(r'^achievement/(?P<achievement_id>\d+)/$', AchievementView.as_view(), name="achievement_view"),
    url(r'^achievement/new/$', login_required(CreateAchievementView.as_view()), name="achievement_new"),
    url(r'^achievement/edit/(?P<achievement_id>\d+)$', login_required(EditAchievementView.as_view()),
        name="achievement_edit"),

    url(r'^news/(?P<news_id>\d+)/$', NewsView.as_view(), name="news_view"),
    url(r'^news/create/$', login_required(CreateNewsView.as_view()), name="news_create"),
    url(r'^news/edit/(?P<news_id>\d+)$', login_required(EditNewsView.as_view()), name="news_edit"),
    url(r'^news/editinline/(?P<news_id>\d+)$', login_required(EditNewsViewInline.as_view()), name="news_edit_inline"),
    # url(r'^all/$', PublicationsList.as_view(), name="user_publications"),
]