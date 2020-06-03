from django.views.generic import TemplateView


class PagesMainView(TemplateView):
    template_name = "index.html"
