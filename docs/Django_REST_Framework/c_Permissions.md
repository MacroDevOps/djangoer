## Permissions

### 主要判断依据
1. 在执行视图的 dispatch() 方法前，会先进行视图访问权限的判断
2. 在经过 get_object() 获取具体对象时，会进行对象访问权限的判断

### 权限类型
1. AllowAny 容许全部用户
2. IsAuthenticated 仅经过认证的用户
3. IsAdminUser 仅管理员用户
4. IsAuthenticatedOrReadOnly 认证的用户能够彻底操做，不然只能get读取

### 使用方法
1. 能够在配置文件中设置默认的权限管理类
```shell
REST_FRAMEWORK = {
    'DEFAULT_PERMISSION_CLASSES': (
        'rest_framework.permissions.IsAuthenticated',
    )
}
```
2. 具体的视图中经过permission_classes属性来设置
```shell
from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView

class ExampleView(APIView):
    permission_classes = (IsAuthenticated,)
    ...
```

3. 自定义权限
如需自定义权限，需继承rest_framework.permissions.BasePermission父类，并实现如下两个任何一个方法或所有spa

- `.has_permission(self, request, view)rest`

是否能够访问视图， view表示当前视图对象code

- `.has_object_permission(self, request, view, obj)`

是否能够访问数据对象， view表示当前视图， obj为数据对象对象


例如
```python
class MyPermission(BasePermission):
    """
    自定义添加权限控制类
    """
    def has_object_permission(self, request, view, obj):
        """控制对obj对象的访问权限，此案例决绝全部对对象的访问"""
        return False

class BookInfoViewSet(ModelViewSet):
    queryset = BookInfo.objects.all()
    serializer_class = BookInfoSerializer
    permission_classes = [IsAuthenticated, MyPermission]
```
