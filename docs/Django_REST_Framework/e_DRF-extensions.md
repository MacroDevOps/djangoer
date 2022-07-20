## drf-extensions
```shell
pip install drf-extensions
```

### drf-extensions - redis
1. 安装依赖库
```shell
pip install django-redis
```

2. settings.py 配置Redis配置
```shell
CACHES = {
    "default": {
        "BACKEND": "django_redis.cache.RedisCache",
        "LOCATION": "redis://127.0.0.1:6379/",
        "OPTIONS": {
            "CLIENT_CLASS": "django_redis.client.DefaultClient",
            "CONNECTION_POOL_KWARGS": {"max_connections": 100} # 配置连接池
        }
    }
}
```

3. 作为 session backend 使用配置
```python
SESSION_ENGINE = "django.contrib.sessions.backends.cache"
SESSION_CACHE_ALIAS = "default"
```

4. 自定义redis的使用方法
```python

```

1. 对象级权限控制 rules
- [ ][Object level permissions support](https://github.com/dfunckt/django-rules)