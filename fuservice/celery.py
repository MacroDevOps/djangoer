from __future__ import absolute_import, unicode_literals
import os
from celery import Celery, platforms
from fuservice import settings

platforms.C_FORCE_ROOT = True
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'fuservice.settings')
app = Celery('fuservice', broker=settings.CELERY_BROKER_URL, backend=settings.CELERY_RESULT_BACKEND)
app.config_from_object('django.conf.settings')
app.autodiscover_tasks(lambda: settings.INSTALLED_APPS)