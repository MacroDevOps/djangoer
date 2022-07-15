## 视图集
1. GET： retrieve， 获取详情数据（单条）
2. GET ：list， 获取列表数据（多条）
3. POST： create， 创建数据
4. PUT： update 更新数据
5. PATCH： partail_update， 更新部分数据
6. DELETE： destroy， 删除数据

### 各种集成类试图
1. ViewSet
   1. 继承ViewSetMixin和views.APIView
   2. ViewSetMixin支持action动作
   3. 未提供get_onject()、get_serializer()、queryset、serializer_class等，因此不支持过滤、排序和分页的操作
2. GenericViewSet类
   1. 继承ViewSetMixin和generic.GenericAPIView
   2. 提供get_onject()、get_serializer()、queryset、serializer_class等，支持过滤、排序和分页的操作
   3. 在定义路由时，需要将请求方法与action动作进行绑定
   4. 使用Mixin类简化程序、
3. ReadOnlyModelViewSet类
   1. 继承mixins.RetrieveModelMixin、mixins.ListModelMixin和generic.GenericAPIView
4. ModelViewSet类
   1. 继承mixins.CreateModelMixin、mixins.RetrieveModelMixin、mixins.UpdateModelMixin、mixins.DestroyModelMixin、mixins.ListModelMixin和generic.GenericAPIView
   2. 使用ModelViewSet替换所有继承

