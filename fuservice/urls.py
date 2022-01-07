"""fuservice URL Configuration

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
import os
from django.conf.urls import url, include
from django.urls import path
from django.views.generic import RedirectView
from rest_framework import routers
from rest_framework.documentation import include_docs_urls

import xadmin
from fuservice import settings

router = routers.DefaultRouter()

urlpatterns = [
    url(r'^', include(router.urls)),
    url(r'^user', include('user.urls', namespace="user")),
    path('si-service/', include('SIService.urls')),
    url(r'api-auth/', include('rest_framework.urls', namespace='rest_framework')),
    url(r'^xadmin/', xadmin.site.urls),
    url(r'^docs/', include_docs_urls(title="FUService API Docs"), name="docs"),
    url(r'^favicon.ico$', RedirectView.as_view(url=os.path.join(settings.STATIC_URL, "favicon.ico"), permanent=True)),
]
