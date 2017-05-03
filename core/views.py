from django.contrib.contenttypes.models import ContentType
from django.shortcuts import render, resolve_url
from core.models import User
from django.views.generic import ListView, DetailView, TemplateView, CreateView
from publications.models import PublicationMetaInfo, Achievement, News
from .forms import UserRegistrationForm


class MainPage(TemplateView):
    template_name = 'core/main_page.html'

    def get_context_data(self, **kwargs):
        context = super(MainPage, self).get_context_data(**kwargs)
        context["last_news"] = News.objects.last()  # sorted be order_by("-creation_date")
        # if not context["last_news"]:
        #     context["last_news"] = News()
        context["last_achievement"] = Achievement.objects.last()  # sorted be order_by("-creation_date")
        return context


class UsersList(ListView):
    model = User
    # paginate_by = 20
    template_name = "users/all_users.html"


class UserView(DetailView):
    model = User
    template_name = "users/one_user.html"
    pk_url_kwarg = "user_id"
    context_object_name = "user_profile"

    def get_context_data(self, **kwargs):
        context = super(UserView, self).get_context_data(**kwargs)
        last_publications = PublicationMetaInfo.objects.filter(author=self.get_object().id)
        last_publications = last_publications.order_by('-update_date')[:5]
        if last_publications.count() > 0:
            context["last_publications"] = last_publications
        context["achievement_content_type"] = ContentType.objects.get_for_model(Achievement)
        context["news_content_type"] = ContentType.objects.get_for_model(News)
        return context


class UserRegistrationView(CreateView):
    form_class = UserRegistrationForm
    template_name = 'users/new_user.html'

    def get_success_url(self):
        return resolve_url('core:main_page')

    # def form_valid(self, form):
    #     return super(UserRegistrationForm, self).form_valid(form)
