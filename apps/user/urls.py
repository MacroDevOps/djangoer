from django.conf.urls import url
from rest_framework import routers
from rest_framework_jwt.views import obtain_jwt_token

from . import views
from .views import UserViewSet, send_email

router = routers.DefaultRouter()
router.register(r'', UserViewSet, basename='userinfo')

app_name = 'user'

urlpatterns = [
    url('email/', send_email, name="send_email"),
    url('login/', obtain_jwt_token, name="login"),
    url(r'^base$', views.MyBase.as_view()),
]
