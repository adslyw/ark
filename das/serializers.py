# -*- coding: utf-8 -*-
from rest_framework import serializers
from das.models import *

class HomePageSerializer(serializers.Serializer):
    # personal_rank = serializers.IntegerField(label='高考位次')
    subject_type = serializers.ChoiceField(
        label='考生类型',
        choices=[(s.type_name, s.type_name) for s in SubjectType.objects.all()],
        # style={'class': 'selectpicker'}
    )

    batch_name = serializers.ChoiceField(
        label='录取批次',
        choices=[(a.batch_name, a.batch_name) for a in AdmissionBatch.objects.all()],
        # style={'class': 'selectpicker'}
    )

    score = serializers.IntegerField(label='高考分数')

class HomePage2Serializer(serializers.Serializer):
    subject_type = serializers.ChoiceField(
        label='考生类型',
        choices=[(s.type_name, s.type_name) for s in SubjectType.objects.all()],
        # style={'class': 'selectpicker'}
    )

    batch_name = serializers.ChoiceField(
        label='录取批次',
        choices=[(a.batch_name, a.batch_name) for a in AdmissionBatch.objects.all()],
        # style={'class': 'selectpicker'}
    )

    personal_rank = serializers.IntegerField(label='高考位次')
