#!/usr/bin/env python
# encoding: utf-8
from xadmin import views
from .models import UserProfile, TeamInfo, OrganizationInfo

from django_celery_beat.models import IntervalSchedule, CrontabSchedule, ClockedSchedule, PeriodicTask
from django_celery_results.models import TaskResult

import xadmin

"""
choose icon from https://fontawesome.com/v4.7.0/icons/
"""


class IntervalScheduleAdmin(object):
    list_display = [
        'id', 'every', 'period',
    ]
    ordering = ['id']
    search_fields = ['every']
    list_per_page = 10
    model_icon = 'fa fa-clock-o'


class CrontabScheduleAdmin(object):
    list_display = [
        'id', 'minute', 'hour',
        'day_of_week', 'day_of_month', 'month_of_year', 'timezone'
    ]
    ordering = ['id']
    search_fields = ['minute']
    list_per_page = 10
    model_icon = 'fa fa-clock-o'


class SolarScheduleAdmin(object):
    list_display = [
        'id', 'event', 'latitude', 'longitude'
    ]
    ordering = ['id']
    search_fields = ['event']
    list_per_page = 10
    model_icon = 'fa fa-wrench'


class ClockedScheduleAdmin(object):
    list_display = [
        'id', 'clocked_time'
    ]
    ordering = ['id']
    search_fields = ['clocked_time']
    list_per_page = 10
    model_icon = 'fa fa-clock-o'


class PeriodicTaskAdmin(object):
    list_display = [
        'id', 'name', 'task', 'args', 'kwargs', 'queue',
        'exchange', 'routing_key', 'expires', 'enabled',
        'last_run_at', 'total_run_count', 'date_changed', 'description',
        'interval', 'crontab', 'solar', 'clocked', 'one_off',
        'start_time', 'priority', 'headers'
    ]
    ordering = ['id']
    search_fields = ['name']
    list_per_page = 10
    model_icon = 'fa fa-tasks'


class TaskResultAdmin(object):
    list_display = [
        'id', 'task_id', 'status', 'content_type', 'content_encoding',
        'result', 'date_done', 'traceback', 'meta',
        'task_args', 'task_kwargs', 'task_name'
    ]
    ordering = ['id']
    search_fields = ['task_id']
    list_per_page = 10
    model_icon = 'fa fa-book'


class BaseSetting(object):
    enable_themes = True
    use_bootswatch = True


class GlobalSettings(object):
    site_title = "Flow"
    site_footer = "djangoer@durgin.cn"
    menu_style = "accordion"


class UserSettingsAdmin(object):
    list_display = ['username', 'birthday', 'gender', 'mobile', 'email']
    model_icon = 'fa fa-user'


class TeamInfoAdmin(object):
    list_display = ["team_name", "organization", "create_time"]
    model_icon = 'fa fa-address-book'


class OrganizationInfoAdmin(object):
    list_display = ["name", "create_time"]
    model_icon = 'fa fa-university'


xadmin.site.register(IntervalSchedule, IntervalScheduleAdmin)
# 间隔时间表
xadmin.site.register(CrontabSchedule, CrontabScheduleAdmin)
# 定时时间表
xadmin.site.register(ClockedSchedule, ClockedScheduleAdmin)
# 计时时间表
xadmin.site.register(PeriodicTask, PeriodicTaskAdmin)
# 配置任务
xadmin.site.register(TaskResult, TaskResultAdmin)
# 任务结果
xadmin.site.unregister(UserProfile)
xadmin.site.register(UserProfile, UserSettingsAdmin)
xadmin.site.register(TeamInfo, TeamInfoAdmin)
xadmin.site.register(OrganizationInfo, OrganizationInfoAdmin)
xadmin.site.register(views.BaseAdminView, BaseSetting)
xadmin.site.register(views.CommAdminView, GlobalSettings)
