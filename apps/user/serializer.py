from rest_framework import serializers


# Serializers define the API representation.
from user.models import UserProfile


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserProfile
        fields = ["id", 'username', 'email', 'is_staff', "user_type"]
