# coding: utf-8
from django.contrib.contenttypes.models import ContentType
from django.shortcuts import resolve_url
from django.views.generic import ListView, DetailView, CreateView, UpdateView

from publications.forms import NewsForm
from .models import News


class CreateNewsView(CreateView):
    model = News
    form_class = NewsForm
    template_name = "publications/type/news/create_new.html"

    # def get_context_data(self, **kwargs):
    #     context = super(AchievementCreateView.self).get_context_data(**kwargs)
    #     # context['form'] = AchievementForm()
    #     return context

    def form_valid(self, form):
        form.instance.author = self.request.user
        print "FIELDS:", form.fields
        # form.instance.publication_type = form.fields
        return super(CreateNewsView, self).form_valid(form)

    def get_success_url(self):
        return resolve_url('publications:all')


class EditNewsView(UpdateView):
    model = News
    form_class = NewsForm
    template_name = "publications/type/news/edit.html"
    pk_url_kwarg = 'news_id'

    def get_queryset(self):
        qs = super(EditNewsView, self).get_queryset()
        qs = qs.filter(author=self.request.user)
        return qs

    def get_success_url(self):
        return resolve_url('publications:all')
