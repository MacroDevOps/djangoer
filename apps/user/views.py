from django.core.cache import cache
from django.forms import models
from django.http import JsonResponse
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.generics import GenericAPIView
from rest_framework import status
from rest_framework.mixins import ListModelMixin

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


class MyBase1(APIView):
    def get(self, request):
        # 1. 查数据
        users = UserProfile.objects.all()
        # 2. 序列化
        serializer = UserSerializer(instance=users, many=True)
        # 3. 返回数据
        return Response(data=serializer.data, status=200)

    def get(self, request, pk):
        # 1. 查数据
        try:
            user = UserProfile.objects.get(pk=pk)
        except UserProfile.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)

        # 2. 序列化
        serializer = UserSerializer(instance=user)

        # 3. 返回数据
        return Response(data=serializer.data, status=status.HTTP_200_OK)

    def put(self, request, pk):
        # 0.  获取数据
        data = request.data
        # 1. 查数据
        try:
            user = UserProfile.objects.get(pk=pk)
        except UserProfile.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)
        # 2. 反序列化
        serializer = UserSerializer(data=data)
        serializer.is_valid(raise_exception=True)
        # 3. update
        serializer.save()
        return Response(data=data, status=status.HTTP_202_ACCEPTED)

    def post(self, request):
        # 1. 接收数据
        # 2. 反序列化
        # 3. 存数据
        # 4. 返回消息
        return Response({"message": "Ha Ha"}, status=status.HTTP_201_CREATED)

    def patch(self, request, pk):
        # 1. 查数据
        # 2. 反序列化
        # 3. update
        return Response({"message": "Ha Ha"})

    def delete(self, request, pk):
        # 1. 查数据
        # 2. delete
        return Response({"message": "Ha Ha"})


class UserGenView(GenericAPIView):
    queryset = UserProfile.objects.all()
    serializer_class = UserSerializer

    def get(self, request):
        user_list = self.get_queryset()
        serializer = self.get_serializer(instance=user_list, many=True)
        return Response(data=serializer.data, status=status.HTTP_200_OK)

    def post(self, request):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(data=serializer.data, status=status.HTTP_201_CREATED)


class UserGenInfoView(GenericAPIView):
    queryset = UserProfile.objects.all()
    serializer_class = UserSerializer

    def get(self, request, pk):
        user = self.get_object()
        serializer = self.get_serializer(instance=user)
        return Response(data=serializer.data, status=status.HTTP_200_OK)

    def put(self, request, pk):
        user = self.get_object()
        serializer = self.get_serializer(instance=user, data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(data=serializer.data, status=status.HTTP_200_OK)

    def delete(self, request, pk):
        self.get_object().delete()
        return Response(status=status.HTTP_404_NOT_FOUND)


"""
使用DRF的模型扩展类进行操作, GenericAPIView结合相关Mixin的可以简写代码。
"""

from rest_framework.mixins import ListModelMixin, CreateModelMixin, DestroyModelMixin, RetrieveModelMixin, UpdateModelMixin


class UserExtGenView(GenericAPIView, ListModelMixin, CreateModelMixin):
    queryset = UserProfile.objects.all()
    serializer_class = UserSerializer

    def get(self, request):
        return self.list(request)

    def post(self, request):
        return self.create(request)


class UserExtGenViewPk(GenericAPIView, ListModelMixin, DestroyModelMixin, RetrieveModelMixin, UpdateModelMixin):
    queryset = UserProfile.objects.all()
    serializer_class = UserSerializer

    def get(self, request, pk):
        return self.list(request, pk)

    def put(self, request, pk):
        return self.update(request, pk)

    def delete(self, request, pk):
        return self.destroy(request, pk)

"""

"""
from rest_framework.generics import ListAPIView, CreateAPIView, UpdateAPIView, RetrieveUpdateDestroyAPIView


class UserViewSets(ListAPIView, CreateAPIView):
    queryset = UserProfile.objects.all()
    serializer_class = UserSerializer

from rest_framework.viewsets import ViewSet


