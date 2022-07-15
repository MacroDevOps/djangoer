from __future__ import absolute_import, unicode_literals
import os
from abc import ABC

from celery import Celery, platforms, Task
from celery_once import QueueOnce

from djangoer import settings

platforms.C_FORCE_ROOT = True
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'djangoer.settings')
app = Celery('djangoer', broker=settings.CELERY_BROKER_URL, backend=settings.CELERY_RESULT_BACKEND)
app.config_from_object('django.conf.settings')
app.autodiscover_tasks(lambda: settings.INSTALLED_APPS)

custom_log = settings.custom_log


class CustomTask(Task, ABC):
    def on_success(self, retval, task_id, args, kwargs):
        """
        celery life cycle when task on success
        """
        custom_log.info(f"tasks_name: {self.name} tasks_id: {task_id} status >>>>>>: {retval}, args: {args}, kwargs: {kwargs}")
        return super(CustomTask, self).on_success(retval, task_id, args, kwargs)

    def on_retry(self, exc, task_id, args, kwargs, einfo):
        """
        celery life cycle when task on retry
        """
        custom_log.info(f"tasks_name: {self.name} tasks_id: {task_id} einfo >>>>>>: {einfo}, args: {args}, kwargs: {kwargs}")
        return super(CustomTask, self).on_failure(exc, task_id, args, kwargs, einfo)

    def on_failure(self, exc, task_id, args, kwargs, einfo):
        """
        celery life cycle when task on failure
        """
        custom_log.info(f"tasks_name: {self.name} tasks_id: {task_id} einfo >>>>>>: {einfo}, args: {args}, kwargs: {kwargs}")
        return super(CustomTask, self).on_failure(exc, task_id, args, kwargs, einfo)

    def after_return(self, status, retval, task_id, args, kwargs, einfo):
        """
        celery life cycle when task end
        """
        custom_log.info(f"tasks_name: {self.name} tasks_id: {task_id} status >>>>>>: {retval}, args: {args}, kwargs: {kwargs}")
        return super(CustomTask, self).after_return(status, retval, task_id, args, kwargs, einfo)


class CustomOnceTask(QueueOnce, Task, ABC):
    def on_success(self, retval, task_id, args, kwargs):
        """
        celery life cycle when task on success
        """
        custom_log.info(f"tasks_name: {self.name} tasks_id: {task_id} status >>>>>>: {retval}, args: {args}, kwargs: {kwargs}")
        return super(CustomOnceTask, self).on_success(retval, task_id, args, kwargs)

    def on_retry(self, exc, task_id, args, kwargs, einfo):
        """
        celery life cycle when task on retry
        """
        custom_log.info(f"tasks_name: {self.name} tasks_id: {task_id} einfo >>>>>>: {einfo}, args: {args}, kwargs: {kwargs}")
        return super(CustomOnceTask, self).on_failure(exc, task_id, args, kwargs, einfo)

    def on_failure(self, exc, task_id, args, kwargs, einfo):
        """
        celery life cycle when task on failure
        """
        custom_log.info(f"tasks_name: {self.name} tasks_id: {task_id} einfo >>>>>>: {einfo}, args: {args}, kwargs: {kwargs}")
        return super(CustomOnceTask, self).on_failure(exc, task_id, args, kwargs, einfo)

    def after_return(self, status, retval, task_id, args, kwargs, einfo):
        """
        celery life cycle when task end
        """
        custom_log.info(f"tasks_name: {self.name} tasks_id: {task_id} status >>>>>>: {retval}, args: {args}, kwargs: {kwargs}")
        return super(CustomOnceTask, self).after_return(status, retval, task_id, args, kwargs, einfo)