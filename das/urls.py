# -*- coding: utf-8 -*-
from django.urls import path

from das.views import *

urlpatterns = [
    path(r'home/', HomePageView.as_view(), name='home'),
    path(r'home2/', HomePage2View.as_view(), name='home2'),
]
