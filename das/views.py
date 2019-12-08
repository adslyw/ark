# -*- coding: utf-8 -*-
from rest_framework.renderers import TemplateHTMLRenderer
from rest_framework.response import Response
from rest_framework.views import APIView
from das.serializers import *
from das.utils.tools import *

class HomePageView(APIView):
    renderer_classes = [TemplateHTMLRenderer]
    template_name = 'das/home.html'

    def get(self, request):
        serializer = HomePageSerializer()
        return Response({'serializer': serializer})

    def post(self, request):
        serializer = HomePageSerializer(data=request.data)

        if not serializer.is_valid():
            return Response({'serializer': serializer})

        score_difference_value = fetch_score_difference_value(
            serializer.data.get('score'),
            serializer.data.get('batch_name'),
            serializer.data.get('subject_type'),
            '2019'
        )

        recommends = fetch_recommend_univercity(
            score_difference_value,
            serializer.data.get('batch_name'),
            serializer.data.get('subject_type'),
            '2019'
        )

        result = {
            'score': serializer.data.get('score'),
            'personal_rank': serializer.data.get('personal_rank'),
            'subject_type': serializer.data.get('subject_type_name'),
            'score_difference_value': score_difference_value,
            'recommends': recommends
        }

        return Response({'serializer': serializer, 'result': result})
