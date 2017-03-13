from django.shortcuts import render
from django.views.generic import ListView
from posts.models import Profile

def mainPage(request):
    profiles_count = Profile.objects.all().count()
    return render(request, 'core/main_page.html', {'profiles_count':profiles_count})

