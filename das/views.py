# -*- coding: utf-8 -*-
# from django.shortcuts import render
# from django.contrib import messages
# from django.views.generic import (
# 	TemplateView,
# 	FormView,
# )
# from das.forms import *

# # Create your views here.
# class HomePageView(FormView):
#     template_name = "das/home.html"
#     form_class = HomeForm
#     success_url = '.'

#     def get_context_data(self, **kwargs):
#         context = super().get_context_data(**kwargs)
#         messages.info(self.request, "hello")

#         return context

from rest_framework.renderers import TemplateHTMLRenderer
from rest_framework.response import Response
from rest_framework.views import APIView
from das.serializers import *

class HomePageView(APIView):
    renderer_classes = [TemplateHTMLRenderer]
    template_name = 'das/home.html'

    def get(self, request):
        serializer = HomePageSerializer()
        return Response({'serializer': serializer})

