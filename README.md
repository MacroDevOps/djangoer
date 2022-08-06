Encapsulated django restful api basic template
---
> 一套集成了常见工具的django restful API 开发模板，快速实现你想要的drf api接口。

现已集成的组件有
- [x] xadmin 
- [x] celery
- [x] celery 定时任务组件
- [x] DjangoEditor

> 如果你的机器有docker快速体验方式

1. 下载代码
```shell
git clone https://github.com/MacroDevOps/djangoer.git
```
2. docker-compose up 启动服务。
```shell
docker-compose up --build -d
```
3. 体验页面
```shell
# 首页
http://127.0.0.1/

# 文档页面
http://127.0.0.1/docs/

# admin 页面 
http://127.0.0.1/xadmin/
# username: lidj passwd:12345
```

4. windows 下的调试命令
```shell
# 1. 启动 django service
python manage.py runserver 127.0.0.1:8000
# ! 如果你用的编辑器是pycharm本项目自带的的run下有一些非常方便的启动命令，可以支撑你更快的搭建开发环境


# 2. 启动 django celery
celery -A djangoer worker -l info

# 3. django beat 
celery -A djangoer beat -l info
```