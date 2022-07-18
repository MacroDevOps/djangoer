from django.core.cache import cache
from django.http import JsonResponse
from rest_framework.response import Response
from rest_framework.views import APIView

from djangoer.settings import custom_log
from . import tasks
from .models import UserProfile
from rest_framework import viewsets


# ViewSets define the view behavior.
from .serializer import UserSerializer


class UserViewSet(viewsets.ModelViewSet):
    queryset = UserProfile.objects.all()
    serializer_class = UserSerializer


def send_email(request, *args, **kwargs):
    res = tasks.send_email.delay("durgin", "hello world", ["dejinx@qq.com", ])
    return JsonResponse({'status': 'successful', 'task_id': res.task_id})


class MyBase(APIView):
    """
    最基础的API测试连接。

    """
    def get(self, request, name):
        if cache.get("message"):
            custom_log.warning("{user}: 发布了devops最新系统".format(user=request.user))
            return Response({"message": cache.get("message")})
        else:
            cache.set("message", f"{name} Ha Ha", timeout=10)
            print("设置缓存")
            return Response({"message": "Ha Ha"})


class SendEmail(APIView):
    def get(self, request):
        title = request.GET.get('title', None)
        message = request.GET.get('message', None)
        res = tasks.send_email.delay(title, message, ["dejinx@qq.com", ])
        return JsonResponse({'status': 'successful', 'task_id': res.task_id})