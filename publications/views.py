# coding: utf-8
from django.contrib.contenttypes.models import ContentType
from django.views.generic import ListView, DetailView, CreateView, UpdateView
from .forms import *
from .models import Publication, Achievement, News, PublicationMetaInfo
from comments.models import Comment
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
    context_object_name = "publication"
    model = News
    template_name = "publications/type/news/news_view.html"
    pk_url_kwarg = "news_id"

    def get_context_data(self, **kwargs):
        comments = self.get_object().comments.all()
        context = super(NewsView, self).get_context_data(**kwargs)
        context["comments"] = comments
        return context


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
        context["sortform"] = self.sortform
        context["achievement_content_type"] = ContentType.objects.get_for_model(Achievement)
        context["news_content_type"] = ContentType.objects.get_for_model(News)
        return context

    def get_queryset(self):
        # query_set = super(PublicationsList,self).get_queryset()
        if self.sortform.is_valid():
            print "IN GET_QUERYSET, FORM IS VALID"
            initial_queryset = self.get_initial_queryset()
            if self.sortform.cleaned_data['search']:
                qs = initial_queryset.filter(title__icontains=self.sortform.cleaned_data['search']).order_by(
                    self.sortform.cleaned_data['sort'])[:self.paginate_by]
            else:
                qs = initial_queryset.order_by(self.sortform.cleaned_data['sort'])[:self.paginate_by]
            return qs
        else:
            print "IN GET_QUERYSET, FORM INVALID", type(self.sortform.errors), len(self.sortform.errors)
            return super(PublicationsList, self).get_queryset()

    def get_initial_queryset(self):
        types = self.sortform.cleaned_data["publication_type"]
        print "TYPES: ", types
        if len(types) == len(AVAILABLE_PUBLICATIONS_TYPES):
            return PublicationMetaInfo.objects.all()  # все виды публикаций
        else:
            if u'news' in types:
                news_type = ContentType.objects.get_for_model(News)
                return PublicationMetaInfo.objects.filter(content_type=news_type)
            elif u'achievement' in types:
                achievement_type = ContentType.objects.get_for_model(Achievement)
                return PublicationMetaInfo.objects.filter(content_type=achievement_type)
            else:
                return PublicationMetaInfo.objects.all()


# class PublicationCreateView(CreateView):
#     # model = Publication
#     # form_class = PublicationForm
#     # fields = ['title', 'content']
#     # tags = forms.MultipleChoiceField(choices=Tag.objects.all())
#     # publication_type = forms.ChoiceField(choices=AVAILABLE_PUBLICATIONS_TYPES)
#     template_name = "publications/publication_create.html"
#
#     def form_valid(self, form):
#         form.instance.author = self.request.user
#         print "FIELDS:", form.fields
#         # form.instance.publication_type = form.fields
#         return super(PublicationCreateView, self).form_valid(form)
#
#     def get_success_url(self):
#         return resolve_url('publications:all')


class AchievementCreateView(CreateView):
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
        return super(AchievementCreateView, self).form_valid(form)

    def get_success_url(self):
        return resolve_url('publications:all')
