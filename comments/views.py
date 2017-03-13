from django.shortcuts import render
from django.views.generic import DetailView
from .models import Comment

class CommentView(DetailView):
    queryset = Comment.objects.all()

# Create your views here.
