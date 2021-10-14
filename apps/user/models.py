import django
from django.db import models
from django.contrib.auth.models import AbstractUser

USER_TYPE = (
    (1, "consumer"),
    (2, "teamOnwer"),
    (3, "organizeOnwer")
)


class OrganizationInfo(models.Model):
    name = models.CharField(max_length=50, blank=True, null=True, verbose_name="组织名称")
    update_time = models.DateTimeField(db_column="update_time", default=django.utils.timezone.now, max_length=50,
                                       verbose_name="修改时间")
    create_time = models.DateTimeField(db_column="create_time", default=django.utils.timezone.now, max_length=50,
                                       verbose_name="创建时间")

    class Meta:
        verbose_name = "组织"
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.name


class TeamInfo(models.Model):
    team_name = models.CharField(max_length=50, blank=True, null=True, verbose_name="团队名称")
    organization = models.ForeignKey(OrganizationInfo, models.DO_NOTHING, db_column="organization", blank=True,
                                     null=True, verbose_name="公司")
    update_time = models.DateTimeField(db_column="update_time", default=django.utils.timezone.now, max_length=50,
                                       verbose_name="修改时间")
    create_time = models.DateTimeField(db_column="create_time", default=django.utils.timezone.now, max_length=50,
                                       verbose_name="创建时间")

    class Meta:
        verbose_name = "团队"
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.team_name


class UserProfile(AbstractUser):
    birthday = models.DateField(null=True, blank=True, verbose_name="出生年月")
    gender = models.CharField(max_length=6, choices=(("male", u"男"), ("female", "女")), default="female",
                              verbose_name="性别")
    team = models.ForeignKey(TeamInfo, models.DO_NOTHING, db_column="organization", blank=True,
                             null=True, verbose_name="团队")
    user_type = models.IntegerField(choices=USER_TYPE, default=1, verbose_name="用户类型")
    mobile = models.CharField(null=True, blank=True, max_length=11, verbose_name="电话")
    update_time = models.DateTimeField(db_column="update_time", default=django.utils.timezone.now, max_length=50,
                                       verbose_name="修改时间")
    create_time = models.DateTimeField(db_column="create_time", default=django.utils.timezone.now, max_length=50,
                                       verbose_name="创建时间")

    class Meta:
        verbose_name = "用户"
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.username
