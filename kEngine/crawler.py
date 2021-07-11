# -*- conding: utf-8 -*-

import requests
from requests import get
import os
import json
import uuid


class URL:
    localdata = 'https://www.localdata.go.kr/datafile/LOCALDATA_NOWMON_XML.zip'
    gomtang = '/rest/localdata/d0100'

# 파일 다운로드
def download(url, file_name=None):
    if not file_name:
        file_name = url.split('/')[-1]
    with open(file_name, "wb") as fi:
        response = get(url)
        fi.write(response.content)
    if os.path.exists(file_name):
        return True
    else:
        return False

# 종승 서버로 전송
def transfer_localdata(url=None, data=None, payload=None):  # post data 는 list 로 받자.
    try:
        # post
        url = url
        headers = {'Content-Type': 'applicatioin/json'}
        if payload is None:
            payload = "{\"request_code\": \"" + str(uuid.uuid1()) + "\", " \
                      "\"data\": " + json.dumps(data, ensure_ascii = False) + "}"

        rs = requests.post(url=url, headers=headers, data=payload)
        ct = rs.json()

        return ct, payload

    except Exception as e:
        print(e.args)
        return '9999', payload

