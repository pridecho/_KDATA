from kZipfile import zipper
from kEngine import crawler
import xml.etree.ElementTree as et
import os
import json
from dexterlog import klogger


def xmlparsing(filename):
    # localdata_cols_list = []
    # localdata_cols_dict = {}

    # category
    xmlfile = os.path.join(path, filename)
    category = str(xmlfile.split('_')[-1]).split('.')[0].encode("cp437").decode("euc-kr")
    if os.path.isfile('{}/ok/{}.json'.format(zipper.zipper.jsonpath, category)): return False, None

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
    row_list = []
    rows = root.findall('body/rows/row')
    for row in rows:
        row_dict = {}
        for ro in row:
            if 'rowNum' == ro.tag: continue
            row_dict[ro.tag] = ro.text
        row_list.append(row_dict)

    ''' column name
    localdata_cols_dict[category] = col_list
    localdata_cols_list.append(localdata_cols_dict)
    with open('col_name.json', 'w', encoding='utf-8') as f:
        f.write(json.dumps(localdata_cols_list, ensure_ascii=False))
    f.close() 
    '''

    with open('{}/ok/{}.json'.format(zipper.zipper.jsonpath, category), 'w', encoding='utf-8') as f:
        f.write(json.dumps(row_list, ensure_ascii=False))
    f.close()
    os.remove(xmlfile)

    return True, row_list


if __name__ == '__main__':
    # xml 파일 다운로드
    ret = False
    while not ret:
        ret = crawler.download(crawler.URL.localdata, zipper.zipper.zpath + '/' + zipper.zipper.zmon)

    # xml 파일 압축 풀기
    zipper.zipper.unzip(period='month')

    # xml parsing
    for path, dir, files in os.walk(zipper.zipper.uzpath):
        for file in files:
            ret, rows = xmlparsing(file)
            if ret:
                for row in rows:
                    print(row)
