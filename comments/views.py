# -*- coding: utf-8 -*-
from django.shortcuts import resolve_url
from django.views.generic import DetailView, CreateView, UpdateView
from django.views.generic import ListView

from publications.publication_type_resolver import *


class CommentsListView(ListView):
    model = Comment
    paginate_by = 20

    def get_queryset(self):
        qs = Comment.objects.filter(good_list__pk=self.args[0])



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
        context['publication'] = self.get_object().content_object
        return context

    def get_success_url(self):
        commenting_object = self.get_object().content_object
        return get_publication_view_url(type(commenting_object), publication_id=commenting_object.id)


class CreateCommentView(CreateView):
    model = Comment
    fields = ['content']
    template_name = "comment/create.html"

    def get_context_data(self, **kwargs):
        context = super(CreateCommentView, self).get_context_data(**kwargs)
        context['publication'] = self.get_commenting_object()
        return context

    def get_commenting_object(self):
        publication_type = ContentType.objects.get_for_model(PUBLICATION_TYPE_TO_MODEL[self.kwargs['publication_type']])
        commenting_object = PublicationMetaInfo.objects.filter(content_type=publication_type,
                                                               object_id=self.kwargs['publication_id'])
        return commenting_object[0].content_object

    def form_valid(self, form):
        form.instance.author = self.request.user
        form.instance.content_object = self.get_commenting_object()
        return super(CreateCommentView, self).form_valid(form)

    def get_success_url(self):
        return get_publication_view_url(self.kwargs['publication_type'], publication_id=self.kwargs['publication_id'])
