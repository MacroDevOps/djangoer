# Django restful serializer

## serializer
> 由数据库中的数据变成json的过程，
1. serializer 是由类方法最基本的序列化方法，所有的其他的序列化都是继承于 Serializer。
```python
class BookSerializer(serializers.Serializer):
    pass
```
### 可用的参数以及选项
```python

```
2. ModelSerializer 是继承于Serializer。
3. 验证代码的对象方法
```python
def vaildate(self, attrs):
    pass

def vaildate_<字段名>(self, data):
    pass
    # returen
```
4. 完成添加操作和更新操作
```python
def create(self, validated_data):
    pass

def update(self, validated_data):
    pass
```
### 注意事项
1. 使用序列化器的时候要注意，序列化器声明了之后，不会自动执行，需要我们在视图中进行调用才行。
2. 序列化器在使用过程中无法直接进行数据接收, 需要我们在视图中实例化序列对象之后进行传递。 
3. 序列化器的字段类似我们之前使用的models
4. 开发restful 的时候序列化其会帮助我们把模型转化成数据字段。
5. drf提供的模型会帮我们把字典转化成json, 或者把客户端发送来转化成字典。

## re-serializer
1. 在反序列化的时候只有对相关的数据进行验证成功之后才可以进行数据的保存。
2. 在获取反序列化数据之前必须调用 `is_valkid()`方法进行验证， 返回True, False
3. 在验证失败的时候可以进行参数校验失败的返回，可以返回字典，包含字段和错误原因。
4. `NON_FIELD_ERRORS_KEY` 进行非字段错误的返回。
5. 验证成功之后，可以使用 **vaildated_data** 属性获取数据。
6. 在定义字段的时候定义每一个字段的类型和参数选项本身就是以重校验。
```python
from rest_framework import serializers

# 共同的方法可以使用这样的调用方式进行验证
def check_function(data):
    return data

class UserSerializer(serializers.Serializer):
    # 1.1. 字段验证
    # id = serializers.IntegerField(required=True, error_messages={"required": "Int，Id is required"})
    # 使用 error_messages 自定义相关的错误信息。
    id = serializers.IntegerField(read_only=True)
    username = serializers.CharField(max_length=10, required=True)
    modile = serializers.CharField(max_length=11, validators=[check_function])
    
    # 1.2. 验证所有的客户端返回的数据， 1. validate 参数名固定 2. attrs 是传入的所有的字符
    # eg: 1. 密码和确认密码的校验 2. 全量的字符串符合字符串。
    def validate(self, attrs):
        print(f"我要验证所有的参数{attrs}")
        return attrs
    
    #1.3. 单个字段的验证方法 1. 必须以 validate_<name>的方式进行, 2. 下面的 is_valid()调用的时候会同步调用。
    # eg: 单个字段特殊的处理
    def validate_mobile(self, value):
        print(value)
        if value[1] != "2":
            raise serializers.ValidationError("第二个字段必须是 2")
        return value
    # 1.4. 公共 特性字段验证
 
    # 2. 数据库入库
    # 前提: 完成验证之后进行数据库入库
    def update(self, instance, validated_data):
        """
        方法名必须是 update， 参数 instance, validated_data
        """
        instance.username = validated_data["username"]
        instance.mobile = validated_data["mobile"]
        instance.save()
        return instance

    # create数据 1. 方法名 create , 2.参数就是验证成功的结果。
    def create(self, validated_data):
        return UserProfile.objects.create(**validated_data)
    
from django.views import View
class UserViewSet(View):
    def get(self, request):
        # 1. 获取客户端的值
        # data = json.dumps(request.body)
        data = {
            "username": "lidjlidjlidjlidjlidjlidj",
            "mobile": "123455"
        }
        # 2.实例化序列化器，获取序列化对象
        serializers = UserSerializer(data = data) # create
        # serializers = UserSerializer(data = data, partial=True) # partial 一些数据不需要验证, 
        # eg: 必须修改密码的时候只是需要验证密码。
        # serializers = UserSerializer(data = data, instance=user) # update
        # 3. 调用实例化验证方法 ·is_valid()进行验证数据, 自定义判断方法就重写这个函数
        # res = serializers.is_valid()
        res = serializers.is_valid(raise_exception=True) # 忽略异常，下面的结构就不需要判断了。 TODO ?
        # 4. 判断并获取数据
        if res:
            print(serializers.validated_data)
            # save 可以传入一些不验证的数据进行保存
            serializers.save()
            return JsonResponse(status=200, data=serializers.validated_data, safe=False)
        else:
            # serializers.errors 根据序列化的结果返回相关的判断依据。
            print(serializers.errors)
```

## 使用Model serializers 简化代码是Serializers的子类。
1. 基于模型类生成一系列的字段
2. 基于模型类自动实现Serializer生成validators, 比如unique_together
3. 默认包含了update和create的实现。

```python




```

### Reference
- [DRF Serializer fields](https://www.django-rest-framework.org/api-guide/fields/)
