from kZipfile import zipper
from kEngine import crawler
import xml.etree.ElementTree as et
import os
import shutil
import json
import hashlib
from dexterlog import klogger


def xmlparsing(filename):
    # localdata_cols_list = []
    # localdata_cols_dict = {}

    xmlfile = os.path.join(path, filename)
    # category
    #     # category = str(xmlfile.split('_')[-1]).split('.')[0].encode("cp437").decode("euc-kr")
    #     # jsonfile = '{}/{}.json'.format(zipper.zipper.jsonpath, category)
    # if os.path.isfile(jsonfile):
    #     os.remove(xmlfile)
    #     return False, None

    # xml root
    tree = et.parse(xmlfile)
    root = tree.getroot()

    # col list
    col_list = []
    cols = root.find('header/columns')
    for col in cols:
        col_list.append(col.tag)

    # data count
    count = int(root.find('header/paging/totalCount').text)

    # row list
    row_common_list = []
    rows = root.findall('body/rows/row')
    for row in rows:
        row_common_dict = {}
        row_unique_dict = {}
        common_flag = True
        for ro in row:
            if common_flag:
                row_common_dict[ro.tag] = ro.text
            else:
                row_unique_dict[ro.tag] = ro.text
            if 'y' == ro.tag: common_flag = False

        row_common_dict["items"] = json.dumps(row_unique_dict, ensure_ascii=False)
        hash = hashlib.md5(json.dumps(row_common_dict, sort_keys=True).encode('utf-8')).hexdigest()
        row_common_dict["data_hash"] = hash

        row_common_list.append(row_common_dict)

    ''' column name
    localdata_cols_dict[category] = col_list
    localdata_cols_list.append(localdata_cols_dict)
    with open('col_name.json', 'w', encoding='utf-8') as f:
        f.write(json.dumps(localdata_cols_list, ensure_ascii=False))
    f.close() 
    '''

    # with open(jsonfile, 'w', encoding='utf-8') as f:
    #     f.write(json.dumps(row_common_list, ensure_ascii=False))
    # f.close()
    # os.remove(jsonfile)
    os.remove(xmlfile)

    return True, row_common_list


if __name__ == '__main__':
    for path, dir, files in os.walk(zipper.zipper.uzpath):
        if 0 == len(files):  # 실패 이력 없을 경우
            # xml 파일 다운로드
            ret = False
            while not ret:
                ret = crawler.download(crawler.URL.localdata, os.path.join(zipper.zipper.zpath, zipper.zipper.zmon))

            # xml 파일 압축 풀기
            zipper.zipper.unzip(period='month')

            # xml 압축파일 백업
            shutil.move(os.path.join(zipper.zipper.zpath, zipper.zipper.zmon),
                        os.path.join(zipper.zipper.backupzpath, zipper.zipper.backupzmon))

    # xml parsing
    for path, dir, files in os.walk(zipper.zipper.uzpath):
        for file in files:
            ret, rows = xmlparsing(file)
            if ret:
                for row in rows:
                    ret, payload = crawler.transfer_localdata(crawler.URL.gomtang, row, payload=None)
                    if '9999' == ret:
                        ng_payload = '{}/{}_{}.json'.format(zipper.zipper.jsonpath, row["opnSvcNm"], row["rowNum"])
                        with open(ng_payload, 'w', encoding='utf-8') as f:
                            f.write(payload)
                        f.close()
                    else:
                        print(ret)


