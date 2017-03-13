from django.shortcuts import render
from django.urls import reverse

from  .models import Profile, Publication
from django.views.generic import ListView, DetailView
# Create your views here.

class PublicationsList(ListView):
    queryset = Publication.objects.all()
    paginate_by = 10
    # template_name =

class ProfilesList(ListView):
    queryset = Profile.objects.all()
    # model = Profile
    paginate_by = 5
    template_name = "profiles/all_profiles.html"


class ProfileView(DetailView):
    queryset = Profile.objects.all()
    template_name = "profiles/one_profile.html"

    # def get_context_data(self, **kwargs):
    #     context = super(ProfileView, self).get_context_data(**kwargs)
    #     context["all_profiles_url"] = reverse("posts:all_profiles")
    #     return context


