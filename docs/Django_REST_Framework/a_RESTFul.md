## 视图集
1. GET： retrieve， 获取详情数据（单条）
2. GET ：list， 获取列表数据（多条）
3. POST： create， 创建数据
4. PUT： update 更新数据
5. PATCH： partail_update， 更新部分数据
6. DELETE： destroy， 删除数据

### DRF各种集成类试图
DRF 除了在数据序列化部份的简写之外，还在视图中提供了简写代码的方法，所以在django的 view.View之上Drf还分装了一些必要的功能
  - 控制序列化器的执行 (验证，保存， 数据转换)
  - 控制数据库的操作
  - 调用request和response来操作一些比较扩展的方法。

1. request 和 response
- 内容协商
  - request > parser > 识别客户端请求头中的Content-type来完成数据字典转换 -> 类字典（QueryDict）
  - response > render > 识别客户端请求头中的Accept提取客户端期望的格式 > 返回客户端期望的格式数据。

- **request**
  - DRF中的Request是扩展了Django HttpRequest的方法的Request。
    - **Parser**方法，就可以直接把客户端的内容解析成QueryDict，解析方式是根据前端返回的**Content-type**字段进行匹配的。
    - **.data** 返回解析后的请求体, 类似于 POST FILES等
      - 包含了解析之后的所有数据，文件和非文件。
      - 包含了对POST， PUT, PATCH请求方式解析之后的数据
      - 利用Parser的解析能力支持表单和json数据。
    - **query_params** 查询参数方法, 类似于request.GET 方法 
      - get()
      - getlist()
    - **._request** 的方式可以获取原来的django中的requests 
- **Response** > `rest_framework.response.Response`
  - 内容协商 > accept > context-type > settings default 的顺序进行返回。
  - `render` 渲染相关页面到前面页面。
  - `Response(data={}, status=200, content_type={}, headers={}, template_name="")`
    - data 字典
    - status 状态 `from rest_framework import status` 中有相关的状态返回值
    - content_type 返回类型
    - headers 自定义头
    - template_name 模板

## View 类
### View基类
1. APIView， `from rest_framework.view import APIView`
   1. APIView 与django view之间的不同点。   
      1. 传入到视图方法中的是DRF的request对象， 而不是Django的request。
      2. 返回也是使用的DRF的response对象， 会自动适配前端需要的数据类型，在浏览器的模式下会自动生成相关的文档方式。
      3. 任何的 APIException都会被捕获，并处理成合适的响应信息到客户端。
         1. django
         2. DRF
      4. 重新声明一个新的as_view()的方法，并且在路由分发之前进行身份认证， 鉴权， 流量控制。
         1. django as_view 
         2. drf as_view 
         3. APIView 新增的类
            - **authentication_classes** 身份认证
            - **permission_classes** 权限检查
            - **throttle_classes** 流量控制
      5. get put post create delete

2. GenericAPIView `from rest_framework.generics import GenericAPIView`
   1. 属性 
      1. `serializer_class`序列化类
      2. `queryset` 指明使用的数据查询集
         1. get_queryset() 返回查询集 
         2. get_object() 
            1. 返回详情视图需要的模型类数据对象。
            2. 若详情访问不存在则返回404,
            3. 该方法会使用check_object_permissions检查当前对象是否有访问权限。
      3. pagination_class 分页类
      4. filter_backends 过滤器
   2. 方法 
      1. `get_serializer_class` 获取序列化类
      2. `get_serializer` 获取序列化实例化对象

### View Mixin类 
1. `ListModelMixin` list()
2. `CreateModelMixin` create()
3. `UpdateModelMixin` update()
4. `RetrieveModelMixin` retrieve()
5. `DestroyModelMixin` delete()

### ViewSet 9个试图子类
1. 基础的增删改查
2. 组合方法
```python

```

## drf router 注册
```python
from rest_framework import routers
reouter = routers.DefaultRouter() # 提供了首页的url
routers.SimpleRouter() # 没有提供首页的url
reouter.register("basic", NameVietSet.as_view(), basename="basic")
# [name='userinfo-detail']>, <URLPattern '^$' [name='api-root']>, <URLPattern '^\.(?P<format>[a-z0-9]+)/?$' [name='api-root']>
```

## action 自定义相关
```python
from rest_framework.decorators import action
@action(methods=["GET"], detail=False, url_path="")
def login(self, request):

    return Response()
```

## 嵌套类序列化 - 外键
1. 外键
2. 代码控制外键
3. 嵌套serializer
4. depth=1

