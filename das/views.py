# -*- coding: utf-8 -*-
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

    def post(self, request):
        serializer = HomePageSerializer()
        result = {
            'score': request.data.get('score'),
            'personal_rank': request.data.get('personal_rank'),
            'subject_type': request.data.get('subject_type'),
        }
        return Response({'serializer': serializer, 'result': result})
