from rest_framework import serializers

from book.models import Book, BookFactory
from user.serializer import UserSerializer


class BookFactorySerializer(serializers.ModelSerializer):
    class Meta:
        model = BookFactory
        fields = "__all__"


class BookModelsSerializer(serializers.ModelSerializer):
    factory = BookFactorySerializer(read_only=True)
    username = UserSerializer(read_only=True)

    class Meta:
        model = Book
        fields = "__all__"

    def validate(self, attrs):
        """
        validate_name 验证所有的数据
        """
        print(attrs)
        if attrs.get("name") == "aaa":
            raise serializers.ValidationError({
                "msg": "name is not aaa"
            })
        return attrs

    def validate_name(self, values):
        """
        validate_name 验证数据的方式
        """
        if values == "aaa":
            raise serializers.ValidationError({
                "name": "name is not a book name"
            })
        return values

    def validate_pages(self, values):
        """
        添加一个不存在models的字段
        """
        return self.data.get("name") + self.data.get("name")
