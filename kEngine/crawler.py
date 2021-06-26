import requests
from requests import get
import os
import json


class URL:
    localdata = 'https://www.localdata.go.kr/datafile/LOCALDATA_NOWMON_XML.zip'

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

# rest api
def get_response(url=None, data=None, type=1):  # post data 는 list 로 받자.
    # post
    if type == 1:  # post - normal
        url = url
        data = dict([(k, v) for k, v in zip(data[::2], data[1::2])])
        rs = requests.post(url=url, data=data)
        ct = rs.text
    elif type == 2:  # post - byte -xls down
        url = url
        data = dict([(k, v) for k, v in zip(data[::2], data[1::2])])
        rs = requests.post(url=url, data=data)
        rs.encoding = "utf-8-sig"
        ct = rs.content
    elif type == 3:  # post - kinsight local data string format
        url = url
        headers = {'Content-Type': 'applicatioin/json'}
        # data = json.dumps({
        #     'text': 'dexter',
        #     'num_samples': 5,
        #     'length': 32
        # })
        data = data
        rs = requests.post(url=url, headers=headers, data=data)
        ct = rs.json()
    # get
    elif type == 4:  # get - url
        rs = requests.get(url=url)
        ct = rs.content.decode('euc-kr', 'replace')
    return ct

    # bs4 Sample
    # soup = BeautifulSoup(html, 'html.parser')
    # fields = soup.findAll('h4', {'class': 'fl_le'})
    # for field in fields:
    #     table = field.find_next_sibling('table')
    #     tds = table.find_all('td', {'class': 'txt'})
    #     for td in tds:
    #         itm_cd = td.a['href'].split('=')[1]
    #         crp_nm = td.get_text()
    #         nextTd = td.find_next_sibling('td')
    #         adjValue = nextTd.get_text()
    #     key = i.get('value')
    # .translate('\r\n\t').strip() -> \n\t\r 제거
    # tr = soup.select_one('#statx-data-table > tbody > tr:nth-of-type(24)')
