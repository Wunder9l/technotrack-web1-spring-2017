from django.views.generic import ListView, DetailView, CreateView, UpdateView
from .forms import *
from .models import Publication
from comments.models import Comment
from django.shortcuts import resolve_url


# Create your views here.
class PublicationView(DetailView):
    context_object_name = "publication"
    model = Publication
    template_name = "publications/publication_view.html"
    pk_url_kwarg = "publication_id"

    def get_context_data(self, **kwargs):
        comments = Comment.objects.filter(publication=self.get_object().id).order_by("creation_date")
        context = super(PublicationView, self).get_context_data(**kwargs)
        context["comments"] = comments
        return context


class PublicationsList(ListView):
    model = Publication
    paginate_by = 30
    template_name = "publications/publications_list.html"
    sortform = None

    def dispatch(self, request, *args, **kwargs):
        self.sortform = SortForm(self.request.GET)
        return super(PublicationsList, self).dispatch(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super(PublicationsList,self).get_context_data(**kwargs)
        context["sortform"] = self.sortform
        return context

    def get_queryset(self):
        # query_set = super(PublicationsList,self).get_queryset()
        if self.sortform.is_valid():
            if self.sortform.cleaned_data['search']:
                qs = Publication.objects.all().filter(title__icontains=self.sortform.cleaned_data['search']).order_by(
                    self.sortform.cleaned_data['sort'])[:self.paginate_by]
            else:
                qs = Publication.objects.all().order_by(self.sortform.cleaned_data['sort'])[:self.paginate_by]
            return qs
        return super(PublicationsList, self).get_queryset()


class PublicationCreateView(CreateView):
    model = Publication
    form_class = PublicationForm
    fields = ['title', 'content']
    tags = forms.MultipleChoiceField(choices=Tag.objects.all())
    publication_type = forms.ChoiceField(choices=AVAILABLE_PUBLICATIONS_TYPES)
    template_name = "publications/publication_create.html"

    def form_valid(self, form):
        form.instance.author = self.request.user
        print "FIELDS:",  form.fields
        # form.instance.publication_type = form.fields
        return super(PublicationCreateView, self).form_valid(form)

    def get_success_url(self):
        return resolve_url('publications:all')
