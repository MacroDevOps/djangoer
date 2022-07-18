import django
from django.db import models

from user.models import UserProfile

class BookFactory(models.Model):
    name = models.CharField(max_length=50, null=True, blank=True, verbose_name="name", help_text="String, 出版社名")
    update_time = models.DateTimeField(db_column="update_time", default=django.utils.timezone.now, max_length=50,
                                       verbose_name="修改时间")
    create_time = models.DateTimeField(db_column="create_time", default=django.utils.timezone.now, max_length=50,
                                       verbose_name="创建时间")

    class Meta:
        verbose_name = "出版社"
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.name


class Book(models.Model):
    name = models.CharField(max_length=50, null=True, blank=True, verbose_name="name", help_text="String, 图书名称")
    author= models.CharField(max_length=50, null=True,  blank=True, verbose_name="author", help_text="String, 图书作者")
    factory = models.ForeignKey(BookFactory, models.DO_NOTHING, blank=True,
                                 null=True, verbose_name="出版社", help_text="Int, 出版社")
    username = models.ForeignKey(UserProfile, models.DO_NOTHING, blank=True,
                                null=True, verbose_name="用户", help_text="Int, 用户")

    update_time = models.DateTimeField(db_column="update_time", default=django.utils.timezone.now, max_length=50,
                                       verbose_name="修改时间")
    create_time = models.DateTimeField(db_column="create_time", default=django.utils.timezone.now, max_length=50,
                                       verbose_name="创建时间")

    class Meta:
        verbose_name = "图书表"
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.name
