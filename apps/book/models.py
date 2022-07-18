import django
from django.db import models

from user.models import UserProfile


class Book(models.Model):
    name = models.CharField(max_length=50, null=True, blank=True, verbose_name="name", help_text="String, 图书名称")
    author= models.CharField(max_length=50, null=True,  blank=True, verbose_name="author", help_text="String, 图书作者")
    username = models.ForeignKey(UserProfile, models.DO_NOTHING, blank=True,
                                 null=True, verbose_name="用户信息", help_text="Int, 用户信息")
    update_time = models.DateTimeField(db_column="update_time", default=django.utils.timezone.now, max_length=50,
                                       verbose_name="修改时间")
    create_time = models.DateTimeField(db_column="create_time", default=django.utils.timezone.now, max_length=50,
                                       verbose_name="创建时间")

    class Meta:
        verbose_name = "图书表"
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.name
