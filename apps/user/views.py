from django.http import JsonResponse

from . import tasks
from .models import UserProfile
from rest_framework import serializers, viewsets


# Serializers define the API representation.
class UserSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = UserProfile
        fields = ["id", 'username', 'email', 'is_staff', "user_type"]


# ViewSets define the view behavior.
class UserViewSet(viewsets.ModelViewSet):
    queryset = UserProfile.objects.all()
    serializer_class = UserSerializer


def send_email(request, *args, **kwargs):
    res = tasks.send_email.delay("durgin", "hello world", ["dejinx@qq.com",])
    return JsonResponse({'status': 'successful', 'task_id': res.task_id})
