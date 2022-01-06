import logging
from abc import ABC

from celery import Task
from django.core.mail import send_mail

from fuservice.settings import EMAIL_FROM
from fuservice.celery import app


class CustomTask(Task, ABC):
    def on_success(self, retval, task_id, args, kwargs):
        print("任务成功")
        return super(CustomTask, self).on_success(retval, task_id, args, kwargs)

    def on_retry(self, exc, task_id, args, kwargs, einfo):
        print("任务重试")
        return super(CustomTask, self).on_failure(exc, task_id, args, kwargs, einfo)

    def on_failure(self, exc, task_id, args, kwargs, einfo):
        print("任务失败")
        return super(CustomTask, self).on_failure(exc, task_id, args, kwargs, einfo)

    def after_return(self, status, retval, task_id, args, kwargs, einfo):
        print("任务跑完")
        return super(CustomTask, self).after_return(status, retval, task_id, args, kwargs, einfo)


@app.task(base=CustomTask)
def send_email(title, message, email_list):
    try:
        send_mail(subject=title, message=message, from_email=EMAIL_FROM, recipient_list=email_list)
        return 'success!'
    except Exception as e:
        logging.error(e)
    """
    subject, message, from_email, recipient_list,
          fail_silently=False, auth_user=None, auth_password=None,
          connection=None, html_message=None
    主题 ，信息，发件人，收件人列表
    """


if __name__ == '__main__':
    subject = "你发送的邮件标题"
    message = '你发送的邮件正文'
    send_mail(subject=subject, recipient_list=['dejinx@qq.com'], from_email=EMAIL_FROM, message=message)
