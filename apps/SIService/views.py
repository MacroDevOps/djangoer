import json
import logging
import os
import sys
import time
import zipfile

from django.http import HttpResponse
from SIService import tasks
from SIService.uitls import request_call_back, upload_file_to_ceph
from fuservice import settings
from .tasks import get_bucket


def get_json(result):
    return HttpResponse(json.dumps(result, ensure_ascii=False))


def upload_file_Oss(bucket, source_file, target_file):
    with open(source_file, 'rb') as f:
        result = bucket.put_object(target_file, f).headers
        return result


def uploadECPHCommonFile(request):
    file_path = request.GET.get("dir", None)
    file = request.FILES.get("file", None)
    ip = request.GET.get("ip", None)
    params = request.GET
    if file:
        if file_path not in ["config", "icon", "version"]:
            result = {
                "success": False,
                "msg": "file dir must be 'config', 'icon', 'version'"
            }
        else:
            target_file = "common/{dir}/{file_name}".format(dir=file_path, file_name=file.name)
            save_path = '{}/temp/{}'.format(settings.MEDIA_ROOT, file.name)
            with open(save_path, 'wb') as f:
                for content in file.chunks():
                    f.write(content)
            upload_file_to_ceph(save_path, target_file)
            if ip is not None:
                request_call_back(params, target_file, ip)
            result = {
                "success": True,
                "msg": "upload is success",
                "params": params
            }
    else:
        result = {
            "success": False,
            "msg": "file is null"
        }
    return get_json(result)

def uploadOSS_common_file(request):
    file_path = request.GET.get("dir", None)
    file = request.FILES.get("file", None)
    ip = request.GET.get("ip", None)
    params = request.GET
    if file:
        if file_path not in ["config", "icon", "version"]:
            result = {
                "success": False,
                "msg": "file dir must be 'config', 'icon', 'version'"
            }
        else:
            target_file = "common/{dir}/{file_name}".format(dir=file_path, file_name=file.name)
            bucket = get_bucket()
            save_path = '{}/temp/{}'.format(settings.MEDIA_ROOT, file.name)
            with open(save_path, 'wb') as f:
                for content in file.chunks():
                    f.write(content)
            upload_file_Oss(bucket, save_path, target_file)
            request_call_back(params, target_file, ip)
            result = {
                "success": True,
                "msg": "upload is success",
                "params": params
            }
    else:
        result = {
            "success": False,
            "msg": "file is null"
        }
    return get_json(result)


def uploadOSS_simple(request):
    result = {}
    if request.method == "POST":
        file = request.FILES.get("file", None)
        file_type = request.POST.get("type", None)
        if not file:
            result = {
                "success": "failed",
                "msg": "file is Nano"
            }
            return get_json(result)
        if file_type not in ["config"]:
            result = {
                "success": "filed",
                "msg": "file_type must be 'config'"
            }
            return get_json(result)
        target_file = "{file_name}".format(file_name=file.name)
        bucket = get_bucket()
        save_path = '{}/temp/{}'.format(settings.MEDIA_ROOT, file.name)
        with open(save_path, 'wb') as f:
            for content in file.chunks():
                f.write(content)
        upload_file_Oss(bucket, save_path, target_file)
        result = {
            "success": "true",
            "msg": "upload is success"
        }
    return get_json(result)


def all_file_scan(unzip_path):
    all_file = []
    for (root, dirs, files) in os.walk(unzip_path):
        for file in files:
            all_file.append(os.path.join(root, file))
    return all_file


def back(obj):
    logging.Logger(obj.result)


def pback(obj):
    logging.Logger(obj.result)


def save_file_local(save_path, file):
    with open(save_path, 'wb') as f:
        for content in file.chunks():
            f.write(content)


def zip2file(zip_file_name: str, extract_path: str, members=None, pwd=None):
    with zipfile.ZipFile(zip_file_name) as zf:
        zf.extractall(extract_path, members=members, pwd=pwd)


def upload_zip(Params, file, detail_path, ip):
    save_path = '{}/temp/{}'.format(settings.MEDIA_ROOT, file.name)
    if sys.platform == "win32":
        save_path = save_path.replace("/", "\\")
    save_file_local(save_path, file)
    if zipfile.is_zipfile(save_path):
        global_key = time.strftime('%Y%m%d%H%M%S', time.localtime())
        unzip_path = os.path.join(settings.MEDIA_ROOT, global_key)
        zip2file(save_path, unzip_path)
        unzip_files = all_file_scan(unzip_path)
        filename = file.name
        res = tasks.upload_zip_to_oss.delay(Params, unzip_files, filename, global_key, detail_path, ip)
        result = {
            "success": "true",
            "msg": "upload file tasks running tasksId: {tasksId}".format(tasksId=res.id)
        }
    else:
        result = {
            "success": "failed",
            "message": "uploaded package is not ZIP package"
        }

    return result


def uploadOSSConfigZip(request):
    if request.method == 'POST':
        file = request.FILES.get("file", None)
    ip = request.GET.get("ip", None)
    params = request.GET
    if file is None:
        result = {"message": "file is null"}
    else:
        detail_path = "common"
        result = upload_zip(params, file, detail_path, ip)
    return get_json(result)


def uploadOSSMiniGamePackage(request):
    if request.method == 'POST':
        file = request.FILES.get("file", None)
    ip = request.GET.get("ip", None)
    path_name = request.GET.get("path", None)
    params = request.GET
    if file is not None:
        if path_name in ["lh-lord-release-out", "lh-lord-debug", "lh-lord-release", "lh-lord", "mt-lord-debug",
                             "mt-lord-release", "mt-lord", "vlord", "xxqjlord-release", "xxqjlord-debug","xxqjchess-release"]:
            result = upload_zip(params, file, path_name, ip)
        else:
            result = {
                "success": False,
                "msg": "path_name need belong to the list [lh-lord-release-out, lh-lord-debug, lh-lord-release, "
                       "lh-lord, mt-lord-debug, mt-lord-release, mt-lord, vlord, xxqjlord-release, xxqjlord-debug, "
                       "xxqjchess-release] "
            }
    else:
        result = {"message": "game package is null"}
    return get_json(result)


def upload_zip_to_ecph(Params, file, detail_path, ip):
    save_path = '{}/temp/{}'.format(settings.MEDIA_ROOT, file.name)
    if sys.platform == "win32":
        save_path = save_path.replace("/", "\\")
    save_file_local(save_path, file)
    if zipfile.is_zipfile(save_path):
        unzip_path = save_path[:-4]
        zip2file(save_path, unzip_path)
        unzip_files = all_file_scan(unzip_path)
        res = tasks.upload_to_mini_file.delay(Params, unzip_files, file.name, detail_path, ip)
        result = {
            "success": "true",
            "msg": "upload file tasks running tasksId: {tasksId}".format(tasksId=res.id)
        }
    else:
        result = {
            "success": "failed",
            "message": "uploaded package is not ZIP package"
        }
    return result


def uploadECPHConfigZip(request):
    if request.method == 'POST':
        file = request.FILES.get("file", None)
    ip = request.GET.get("ip", None)
    params = request.GET
    if file is None:
        result = {"message": "file is null"}
    else:
        detail_path = "common"
        result = upload_zip_to_ecph(params, file, detail_path, ip)
    return get_json(result)
