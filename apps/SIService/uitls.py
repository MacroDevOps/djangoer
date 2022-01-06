import hashlib
import logging
import os
import time
import zipfile

import requests

from fuservice import settings


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


def mkdir_all(path):
    ospath = ""
    for dirname in path.split(os.sep):
        ospath = os.path.join(ospath, dirname)
        if not os.path.exists(ospath):
            print(ospath)
            os.mkdir(ospath)


def zip2file(zip_file_name: str, extract_path: str, members=None, pwd=None):
    with zipfile.ZipFile(zip_file_name) as zf:
        for file in zf.namelist():
            localfilename = '/'.join(file.split('\\'))
            mkdir_all(os.path.join(extract_path, os.path.dirname(localfilename)))
            data = zf.read(file)
            file = open(os.path.join(extract_path, localfilename), 'w+b')
            file.write(data)
            file.close()


def zip2file1(zip_file_name: str, extract_path: str, members=None, pwd=None):
    with zipfile.ZipFile(zip_file_name) as zf:
        zf.extractall(extract_path, members=members, pwd=pwd)


def request_call_back(Params, nums, ip):
    try:
        url_json = 'http://{ip}:3079/uploadcallback'.format(ip=ip)
        data_json = { "status": "success", "file_nums": nums,"param": Params}
        HEADERS = {'Content-Type': 'application/json;charset=utf-8'}
        requests.post(url_json, headers=HEADERS, json=data_json)
        result = True
    except Exception as e:
        result = e
    return result


def upload_file_to_ceph(source_file, target_file):
    url = settings.ECPH_URL
    bucket = settings.BUCKET
    checksum = settings.CHECKSUM
    checksum = checksum + time.strftime("%Y%m%d", time.localtime())
    checksum = hashlib.md5(checksum.encode("utf-8")).hexdigest()
    files = {'file': open(source_file, 'rb')}
    upload_data = {"bucket": bucket, "key": target_file, "ext": os.path.splitext(source_file)[1], "platformID": 0, "userID": 0,
                   "checksum": checksum}
    try:
        upload_res = requests.post(url, upload_data, files=files)
        logging.info(upload_res.json())
    except Exception as e:
        upload_res = {'Code': 0, 'Key': upload_data.get("key"), 'Message': e, 'Ok': False}
        logging.info(upload_res)
    return upload_res.json()


if __name__ == '__main__':
    print(upload_file_to_ceph(
        "C:\\Users\\lidj\\PycharmProjects\\mytest\ceph\\tt_lord_test.json",
        "common/config/test/7c6f7a1b01f812b7f578413bd1e9cda2.json"))