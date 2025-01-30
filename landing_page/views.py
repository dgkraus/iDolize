from django.views.generic import TemplateView

class IndexView(TemplateView):
    template_name = 'landing_page/index.html'
