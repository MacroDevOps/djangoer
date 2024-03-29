"""djangoer URL Configuration

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
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path
from django.views.generic import RedirectView
from rest_framework import routers
from rest_framework.documentation import include_docs_urls

import xadmin
from djangoer import settings

router = routers.DefaultRouter()

urlpatterns = [
    # url(r'^', include(router.urls)),
    url(r'^mdeditor/', include('mdeditor.urls')),
    path('oauth/', include('oauth2_provider.urls', namespace='oauth2_provider')),
    url(r'^user/', include('user.urls', namespace="user")),
    url(r'^book/', include('book.urls', namespace="book")),
    url(r'api-auth/', include('rest_framework.urls', namespace='rest_framework')),
    url(r'^xadmin/', xadmin.site.urls, name="xadmin"),
    url(r'^admin/', admin.site.urls, name="admin"),
    url(r'^docs/', include_docs_urls(title="DevOps API Docs"), name="docs"),
    url(r'^favicon.ico$', RedirectView.as_view(url=os.path.join(settings.STATIC_URL, "favicon.ico"), permanent=True)),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
