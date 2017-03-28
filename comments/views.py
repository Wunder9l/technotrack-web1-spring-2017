from django.shortcuts import render, resolve_url
from django.views.generic import DetailView, CreateView, UpdateView
from publications.models import Publication
from .models import Comment


class CommentView(DetailView):
    queryset = Comment.objects.all()


class EditCommentView(UpdateView):
    model = Comment
    fields = ['content']
    template_name = "comment/edit.html"
    pk_url_kwarg = 'comment_id'

    def get_queryset(self):
        qs = super(EditCommentView, self).get_queryset()
        qs = qs.filter(author=self.request.user)
        return qs

    def get_context_data(self, **kwargs):
        context = super(EditCommentView, self).get_context_data(**kwargs)
        context['publication'] = self.get_object().publication
        return context

    def get_success_url(self):
        return resolve_url('publications:view', publication_id=self.get_object().publication.id)


class CreateCommentView(CreateView):
    model = Comment
    fields = ['content']
    template_name = "comment/create.html"

    def get_context_data(self, **kwargs):
        publication = Publication.objects.get(id=self.kwargs['publication_id'])
        context = super(CreateCommentView, self).get_context_data(**kwargs)
        context['publication'] = publication
        return context

    def form_valid(self, form):
        form.instance.author = self.request.user
        form.instance.publication = Publication.objects.get(
            id=self.kwargs['publication_id'])  # Publication.objects.get(id=self.publication_id)
        return super(CreateCommentView, self).form_valid(form)

    def get_success_url(self):
        return resolve_url('publications:view',
                           publication_id=self.kwargs['publication_id'])
