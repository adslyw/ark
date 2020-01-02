# -*- coding: utf-8 -*-
from rest_framework.renderers import TemplateHTMLRenderer
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.permissions import AllowAny
from das.serializers import *
from das.utils.tools import *

class HomePageView(APIView):
    renderer_classes = [TemplateHTMLRenderer]
    template_name = 'das/home.html'
    permission_classes = (AllowAny,)

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

class HomePage2View(APIView):
    renderer_classes = [TemplateHTMLRenderer]
    template_name = 'das/home2.html'
    permission_classes = (AllowAny,)

    def get(self, request):
        serializer = HomePage2Serializer()
        return Response({'serializer': serializer})

    def post(self, request):
        serializer = HomePage2Serializer(data=request.data)

        if not serializer.is_valid():
            return Response({'serializer': serializer})

        recommends = fetch_recommend_univercity_by_rank(
            int(serializer.data.get('personal_rank')),
            serializer.data.get('batch_name'),
            serializer.data.get('subject_type'),
            '2019'
        )

        rank_difference_value = fetch_rank_difference_value(
            int(serializer.data.get('personal_rank')),
            serializer.data.get('batch_name'),
            serializer.data.get('subject_type'),
            '2019'
        )

        result = {
            'personal_rank': serializer.data.get('personal_rank'),
            'subject_type': serializer.data.get('subject_type_name'),
            'recommends': recommends,
            'rank_difference_value':rank_difference_value,
        }

        return Response({'serializer': serializer, 'result': result})
