# -*- coding: utf-8 -*-
from django.urls import path

from das.views import (
    HomePageView,
)

urlpatterns = [
    path(r'home/', HomePageView.as_view(), name='home'),
]
