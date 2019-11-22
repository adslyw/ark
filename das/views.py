from django.shortcuts import render
from django.contrib import messages
from django.views.generic.base import TemplateView

# Create your views here.
class HomePageView(TemplateView):
    template_name = "das/home.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        messages.info(self.request, "hello")

        return context
