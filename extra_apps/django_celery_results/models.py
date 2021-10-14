"""Database models."""
from __future__ import absolute_import, unicode_literals

import json

from django.conf import settings
from django.db import models
from django.utils.translation import gettext_lazy as _

from celery import states
from celery.result import GroupResult, result_from_tuple

from . import managers

ALL_STATES = sorted(states.ALL_STATES)
TASK_STATE_CHOICES = sorted(zip(ALL_STATES, ALL_STATES))


class TaskResult(models.Model):
    """Task result/status."""

    task_id = models.CharField(
        max_length=getattr(
            settings,
            'DJANGO_CELERY_RESULTS_TASK_ID_MAX_LENGTH',
            255
        ),
        unique=True, db_index=True,
        verbose_name=_('任务ID'),
        help_text=_('Celery正在运行的任务的ID'))
    task_args = models.TextField(
        null=True,
        verbose_name=_('任务位置参数'),
        help_text=_('给任务队列传入的位置参数名: 顺序传参'))
    task_name = models.CharField(
        null=True, max_length=255, db_index=True,
        verbose_name=_('任务名'),
        help_text=_('运行celery是的任务名'))
    task_kwargs = models.TextField(
        null=True,
        verbose_name=_('任务命名参数'),
        help_text=_("传入的命名参数名: 命名传参"))
    status = models.CharField(
        max_length=50, default=states.PENDING, db_index=True,
        choices=TASK_STATE_CHOICES,
        verbose_name=_('任务状态'),
        help_text=_('正在运行的任务的当前状态'))
    worker = models.CharField(
        max_length=100, db_index=True, default=None, null=True,
        verbose_name=_('Worker'), help_text=_('执行任务的Worker')
    )
    content_type = models.CharField(
        max_length=128,
        verbose_name=_('结果内容类型'),
        help_text=_('结果数据的内容类型'))
    content_encoding = models.CharField(
        max_length=64,
        verbose_name=_('结果编码'),
        help_text=_('保存任务结果数据的编码方式'))
    result = models.TextField(
        null=True, default=None, editable=False,
        verbose_name=_('结果数据'),
        help_text=_('任务返回的数据，使用content_encoding和content_type字段读取。'))
    date_created = models.DateTimeField(
        auto_now_add=True, db_index=True,
        verbose_name=_('创建时间'),
        help_text=_('当任务结果以UTC创建时的Datetime字段'))
    date_done = models.DateTimeField(
        auto_now=True, db_index=True,
        verbose_name=_('完成日期时间'),
        help_text=_('当任务以UTC完成时的Datetime字段'))
    traceback = models.TextField(
        blank=True, null=True,
        verbose_name=_('回调'),
        help_text=_('如果任务生成回溯文本，则返回该文本'))
    meta = models.TextField(
        null=True, default=None, editable=False,
        verbose_name=_('任务元信息'),
        help_text=_('关于任务的JSON元信息例如关于儿童任务的信息'))

    objects = managers.TaskResultManager()

    class Meta:
        """Table information."""

        ordering = ['-date_done']

        verbose_name = _('task result')
        verbose_name_plural = _('任务结果')

    def as_dict(self):
        return {
            'task_id': self.task_id,
            'task_name': self.task_name,
            'task_args': self.task_args,
            'task_kwargs': self.task_kwargs,
            'status': self.status,
            'result': self.result,
            'date_done': self.date_done,
            'traceback': self.traceback,
            'meta': self.meta,
            'worker': self.worker
        }

    def __str__(self):
        return '<Task: {0.task_id} ({0.status})>'.format(self)


class ChordCounter(models.Model):
    """Chord synchronisation."""

    group_id = models.CharField(
        max_length=getattr(
            settings,
            "DJANGO_CELERY_RESULTS_TASK_ID_MAX_LENGTH",
            255),
        unique=True,
        db_index=True,
        verbose_name=_("Group ID"),
        help_text=_("Celery ID for the Chord header group"),
    )
    sub_tasks = models.TextField(
        help_text=_(
            "JSON serialized list of task result tuples. "
            "use .group_result() to decode"
        )
    )
    count = models.PositiveIntegerField(
        help_text=_(
            "Starts at len(chord header) and decrements after each task is "
            "finished"
        )
    )

    def group_result(self, app=None):
        """Return the GroupResult of self.

        Arguments:
        ---------
            app (Celery): app instance to create the GroupResult with.

        """
        return GroupResult(
            self.group_id,
            [result_from_tuple(r, app=app)
             for r in json.loads(self.sub_tasks)],
            app=app,
        )
