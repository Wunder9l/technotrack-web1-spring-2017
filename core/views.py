from django.shortcuts import render, resolve_url
from core.models import User
from django.views.generic import ListView, DetailView, TemplateView, CreateView
from publications.models import Publication
from .forms import UserRegistrationForm


class MainPage(TemplateView):
    template_name = 'core/main_page.html'

    def get_context_data(self, **kwargs):
        context = super(MainPage, self).get_context_data(**kwargs)
        users_count = User.objects.all().count()
        context["user_count"] = users_count
        publication_count = Publication.objects.all().count()
        context["publication_count"] = publication_count
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
        last_publications = Publication.objects.filter(author=self.get_object().id).order_by('-update_date')[:5]
        if last_publications.count() > 0:
            context["last_publications"] = last_publications
        return context


class UserRegistrationView(CreateView):
    form_class = UserRegistrationForm
    template_name = 'users/new_user.html'

    def get_success_url(self):
        return resolve_url('core:main_page')

    # def form_valid(self, form):
    #     return super(UserRegistrationForm, self).form_valid(form)
