from django.shortcuts import render
from django.contrib import messages
from django.views.generic import (
	TemplateView,
	FormView,
)
from das.forms import *

# Create your views here.
class HomePageView(FormView):
    template_name = "das/home.html"
    form_class = HomeForm
    success_url = '.'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        messages.info(self.request, "hello")

        return context
