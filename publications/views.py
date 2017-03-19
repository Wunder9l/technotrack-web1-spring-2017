from django.views.generic import ListView, DetailView

from .models import Publication
from comments.models import Comment


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

