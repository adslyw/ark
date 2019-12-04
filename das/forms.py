# -*- coding: utf-8 -*-
from das.models import *
from django import forms
from taggit.forms import TagField
from taggit_labels.widgets import LabelWidget

class UnivercityForm(forms.ModelForm):
    project_tags = TagField(required=False, widget=LabelWidget)

class CityForm(forms.ModelForm):
    tags = TagField(required=False, widget=LabelWidget)

class ProvinceForm(forms.ModelForm):
    tags = TagField(required=False, widget=LabelWidget)
