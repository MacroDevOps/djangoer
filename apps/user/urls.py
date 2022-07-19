from django.conf.urls import url
from django.urls import re_path, include, path
from rest_framework import routers
from rest_framework_jwt.views import obtain_jwt_token

from . import views
from .views import UserViewSet, SendEmail

router = routers.DefaultRouter()
router.register(r'basic', UserViewSet, basename='userinfo')
print(router.urls)
app_name = 'user'

urlpatterns = [
    url(r'^', include(router.urls)),
    url('login/', obtain_jwt_token, name="login"),
    url('base/', views.MyBase.as_view()),
    path('gen_user/', views.UserGenView.as_view()),
    re_path('^gen_user/(?P<pk>\d+)/$', views.UserGenInfoView.as_view()),
    path('mix_user/', views.UserExtGenView.as_view()),
    path('mix_user/<int:pk>/', views.UserExtGenViewPk.as_view()),

    path('set_user/', views.UserViewSets.as_view()),

    path('add_user/', views.UserInfoViewSet.as_view({"get": "get_list", "post": "create_user"})),
    path('add_user/<int:pk>/',
            views.UserInfoViewSetPk.as_view({"get": "user_get", "put": "user_put", "delete": "user_detele"})),

    re_path('^aaa/(?P<pk>\d+)/$', views.MyBase1.as_view()),
    url('send_email/', SendEmail.as_view(), name='send_email'),
]
