from django.conf.urls import url
from .views import CreateCommentView, EditCommentView, CommentsToNews, CommentsToAchievement
from django.contrib.auth.decorators import login_required

urlpatterns = [
    url(r'^create/(?P<publication_type>[a-z]+)/(?P<publication_id>\d+)$',
        login_required(CreateCommentView.as_view()),
        name="create"),
    url(r'^edit/(?P<comment_id>\d+)$', login_required(EditCommentView.as_view()), name="edit"),
    url(r'^to/news/(?P<news_id>\d+)$', CommentsToNews.as_view(), name="news_comments"),
    url(r'^to/achievement/(?P<achievement_id>\d+)$', CommentsToAchievement.as_view(), name="achievement_comments"),

]
