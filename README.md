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
git clone https://github.com/MacroDevOps/fuservice.git
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