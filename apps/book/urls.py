from django.conf.urls import url
from django.urls import include
from rest_framework import routers

from book.views import BookViewSet

router = routers.SimpleRouter()

router.register(r'basic', BookViewSet, basename='book')


app_name = "book"


urlpatterns = [
    url(r'^', include(router.urls)),
]
