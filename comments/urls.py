from django.conf.urls import url
from .views import CreateCommentView, EditCommentView
from django.contrib.auth.decorators import login_required

urlpatterns = [
    url(r'^create/(?P<publication_type>[a-z]+)/(?P<publication_id>\d+)$',
        login_required(CreateCommentView.as_view()),
        name="create"),
    url(r'^edit/(?P<comment_id>\d+)$', login_required(EditCommentView.as_view()), name="edit"),
]
