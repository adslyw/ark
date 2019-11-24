# -*- coding: utf-8 -*-
from das.models import *
from django import forms

class HomeForm(forms.Form):
    score = forms.IntegerField(
    	label='高考分数', 
    	# widget=forms.TextInput(attrs={'class':'form-control'})
    )
    SUBJECT_CHOICES = [(s.id, s.type_name) for s in SubjectType.objects.all()]
    subject_type = forms.ChoiceField(
    	label='考生类型', 
    	choices=SUBJECT_CHOICES, 
    	widget=forms.RadioSelect(),
    )