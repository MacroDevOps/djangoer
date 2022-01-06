from __future__ import absolute_import, unicode_literals

import json
import logging
import os
import sys
import zipfile
from concurrent.futures.thread import ThreadPoolExecutor

import oss2
from celery import shared_task, Task

from SIService.uitls import request_call_back, upload_file_to_ceph
from fuservice import settings
from fuservice.celery import app


def uploadOss(bucket, source_file, target_file):
    with open(source_file, 'rb') as f:
        result = bucket.put_object(target_file, f).headers
        return result


def get_bucket():
    with open(os.path.join(settings.BASE_DIR, "jjlordmtoss.json"), "r", encoding='utf-8') as f:
        data = f.read()
        data = json.loads(data)
        endpoint = data["endpoint"]
        auth = oss2.Auth(data["access_key_id"], data["access_key_secret"])
        bucket = oss2.Bucket(auth, endpoint, "jjlordmt-srv-jj-cn")
    return bucket


def back(obj):
    logging.Logger(obj.result)


def pback(obj):
    logging.Logger(obj.result)


def save_file_local(save_path, file):
    with open(save_path, 'wb') as f:
        for content in file.chunks():
            f.write(content)


def all_file_scan(unzip_path):
    all_file = []
    for (root, dirs, files) in os.walk(unzip_path):
        for file in files:
            all_file.append(os.path.join(root, file))
    return all_file


def zip2file(zip_file_name: str, extract_path: str, members=None, pwd=None):
    with zipfile.ZipFile(zip_file_name) as zf:
        zf.extractall(extract_path, members=members, pwd=pwd)


class CustomTask(Task):
    def on_success(self, retval, task_id, args, kwargs):
        print('异步任务成功')
        return super(CustomTask, self).on_success(retval, task_id, args, kwargs)

    def on_failure(self, exc, task_id, args, kwargs, einfo):
        print('异步任务失败', exc)
        return super(CustomTask, self).on_failure(exc, task_id, args, kwargs, einfo)

    def after_return(self, status, retval, task_id, args, kwargs, einfo):
        print(retval)
        return super(CustomTask, self).after_return(status, retval, task_id, args, kwargs, einfo)


@app.task(base=CustomTask)
def upload_zip_to_oss(Params, unzip_files, filename, global_key, detail_path, ip):
    bucket = get_bucket()
    sum = 0
    with ThreadPoolExecutor(max_workers=30) as pool:
        for unzip_file in unzip_files:
            sum = sum + 1
            if detail_path == "common":
                if sys.platform == "win32":
                    file_abs_patn = unzip_file.split("\\")[unzip_file.split("\\").index(global_key) + 1:]
                else:
                    file_abs_patn = unzip_file.split("/")[unzip_file.split("/").index(global_key) + 1:]
            else:
                if sys.platform == "win32":
                    file_abs_patn = unzip_file.split("\\")[unzip_file.split("\\").index(global_key) + 2:]
                else:
                    file_abs_patn = unzip_file.split("/")[unzip_file.split("/").index(global_key) + 2:]
            t_path = ""
            for item in file_abs_patn:
                t_path = os.path.join(t_path, item)
            unzip_file = unzip_file.replace("\\", "/")
            target_file = "{detail_path}/{unzip_file}".format(detail_path=detail_path, unzip_file=t_path.replace("\\", "/"))
            p = pool.submit(uploadOss, bucket, unzip_file, target_file)
            p.add_done_callback(back)
    if ip is not None:
        call_back = request_call_back(Params, sum, ip)
    else:
        call_back = "ip is null"
    result = {"callbackStatus": call_back,
              "message": "{file_name} count {sum}".format(file_name=filename, sum=sum)}
    return result


@app.task(base=CustomTask)
def upload_to_mini_file(Params, unzip_files, filename, detail_path, ip):
    sum = 0
    for unzip_file in unzip_files:
        sum = sum + 1
        file_abs_patn = unzip_file.split(str(filename)[:-4])[-1][1:]
        target_file = "{detail_path}/{unzip_file}".format(detail_path=detail_path,
                                                         unzip_file=file_abs_patn.replace("\\", "/"))
        upload_file_to_ceph(unzip_file, target_file)
    call_back = request_call_back(Params, sum, ip)
    result = {"callbackStatus": call_back,
              "message": "{file_name} count {sum}".format(file_name=filename, sum=sum)}
    return result