# coding: utf-8
from django.contrib.contenttypes.models import ContentType
from django.db import models
from django.views.generic import ListView, DetailView, CreateView, UpdateView

from publications.publication_type_resolver import PUBLICATION_TYPE_TO_MODEL, PUBLICATION_TYPE_TO_CONTENT_TYPE
from .forms import *
from .models import Publication, Achievement, News, PublicationMetaInfo
from comments.models import Comment
from core.instruments import get_cached_or_qs
from django.shortcuts import resolve_url


# Create your views here.
# class PublicationView(DetailView):
#     context_object_name = "publication"
#     model = Publication
#     template_name = "publications/publication_view.html"
#     pk_url_kwarg = "publication_id"

# def get_context_data(self, **kwargs):
#     comments = self.get_object().comments.all()
#     context = super(PublicationView, self).get_context_data(**kwargs)
#     context["comments"] = comments
#     return context




class PublicationsList(ListView):
    model = PublicationMetaInfo
    paginate_by = 30
    template_name = "publications/publications_list.html"
    sortform = None

    def dispatch(self, request, *args, **kwargs):
        # print "IN DISPATCH: ", self.request.GET
        # if len(self.request.GET) is 0:
        #     self.sortform = SortForm()
        # else:
        #     self.sortform = SortForm(self.request.GET)
        self.sortform = SortForm(self.request.GET)
        return super(PublicationsList, self).dispatch(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super(PublicationsList, self).get_context_data(**kwargs)
        context['total_comments_of_user'] = get_cached_or_qs(
            "total_comments_of_user_{}".format(self.request.user.id),
            Comment.objects.filter(author_id=self.request.user.id).count,
            5)
        context["sortform"] = self.sortform
        return context

    def get_queryset(self):
        # query_set = super(PublicationsList,self).get_queryset()
        if self.sortform.is_valid():
            print "IN GET_QUERYSET, FORM IS VALID"
            qs = self.get_initial_queryset()
            qs = qs.select_related("author").get_published_only_or_all_for_owner(self.request.user)
            qs = qs.prefetch_related("content_object")
            # qs = qs.annotate(comments_count=models.Count('content_object__comments'))
            qs = qs.annotate(
                author_activity=models.Count('author__author_publications') + models.Count('author__author_comments'))

            if self.sortform.cleaned_data['search']:
                qs = qs.filter(title__icontains=self.sortform.cleaned_data['search']).order_by(
                    self.sortform.cleaned_data['sort'])[:self.paginate_by]
            else:
                qs = qs.order_by(self.sortform.cleaned_data['sort'])[:self.paginate_by]
            return qs
        else:
            print "IN GET_QUERYSET, FORM INVALID", type(self.sortform.errors), len(self.sortform.errors)
            return super(PublicationsList, self).get_queryset().get_published_only_or_all_for_owner(self.request.user)

    def get_initial_queryset(self):
        types = self.sortform.cleaned_data["publication_type"]
        chosen_content_types = [PUBLICATION_TYPE_TO_CONTENT_TYPE[key] for key in types]
        return PublicationMetaInfo.objects.filter(content_type__in=chosen_content_types)


class CreateAchievementView(CreateView):
    model = Achievement
    form_class = AchievementForm
    # fields = ['title', 'content']
    template_name = "publications/type/achievement/create_new.html"

    # def get_context_data(self, **kwargs):
    #     context = super(AchievementCreateView.self).get_context_data(**kwargs)
    #     # context['form'] = AchievementForm()
    #     return context

    def form_valid(self, form):
        form.instance.author = self.request.user
        print "FIELDS:", form.fields
        # form.instance.publication_type = form.fields
        return super(CreateAchievementView, self).form_valid(form)

    def get_success_url(self):
        return resolve_url('publications:all')


class EditAchievementView(UpdateView):
    pass


class AchievementView(DetailView):
    context_object_name = "publication"
    model = Achievement
    template_name = "publications/type/achievement/achievement_view.html"
    pk_url_kwarg = "achievement_id"

    def get_context_data(self, **kwargs):
        comments = self.get_object().comments.all()
        context = super(AchievementView, self).get_context_data(**kwargs)
        context["comments"] = comments
        return context


class NewsView(DetailView):
    model = News
    context_object_name = "publication"
    template_name = "publications/type/news/news_view.html"
    pk_url_kwarg = "news_id"

    def get_context_data(self, **kwargs):
        comments = self.get_object().comments.all()
        context = super(NewsView, self).get_context_data(**kwargs)
        context["comments"] = comments
        return context
