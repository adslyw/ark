"""ark URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import include, path
from rest_framework import routers
from square.views import (
    UserViewSet,
    GroupViewSet,
)
from rest_framework_swagger.views import get_swagger_view
from das.views import HomePageView

router = routers.DefaultRouter()
router.register(r'users', UserViewSet)

schema_view = get_swagger_view(title='API')

urlpatterns = [
    path('', HomePageView.as_view(), name='home'),
    path('swagger/', schema_view),
    path('admin/', admin.site.urls),
    path('auth/', include('rest_framework.urls')),
    path('das/', include('das.urls')),
    path('', include(router.urls)),
]

