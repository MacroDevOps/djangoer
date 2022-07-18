from django.conf.urls import url
from django.urls import re_path, include
from rest_framework import routers
from rest_framework_jwt.views import obtain_jwt_token

from . import views
from .views import UserViewSet, SendEmail

router = routers.DefaultRouter()
router.register(r'basic', UserViewSet, basename='userinfo')

app_name = 'user'

urlpatterns = [
    url(r'^', include(router.urls)),
    url('login/', obtain_jwt_token, name="login"),
    re_path(r'^base/(?P<name>\d+)/$', views.MyBase.as_view()),
    url('send_email/', SendEmail.as_view(), name='send_email'),
]
