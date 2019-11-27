# -*- coding: utf-8 -*-
from rest_framework import serializers
from das.models import SubjectType

class HomePageSerializer(serializers.Serializer):
    score = serializers.IntegerField(label='高考分数')
    personal_rank = serializers.IntegerField(label='高考位次')
    subject_type = serializers.ChoiceField(
        label='考生类型',
        choices=[(s.id, s.type_name) for s in SubjectType.objects.all()]
    )
