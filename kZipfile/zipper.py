import zipfile
import os
import datetime
from kSecret.config import config


class Zipper:
    def __init__(self):
        self.root = config['root']
        self.zpath = self.root + 'kZipfile/zip'
        self.backupzpath = self.root + 'kZipfile/zip/backup'
        self.uzpath = self.root + 'kZipfile/unzip'
        self.jsonpath = self.root + 'kZipfile/localdata_json'
        self.zall = 'LOCALDATA_ALL_XML.zip'
        self.zmon = 'LOCALDATA_NOWMON_XML.zip'
        self.backupzmon = 'LOCALDATA_NOWMON_XML_{}.zip'.format(datetime.date.today())

        if not os.path.isdir(self.root):
            os.mkdir(self.root)
        if not os.path.isdir(self.zpath):
            os.mkdir(self.zpath)
        if not os.path.isdir(self.backupzpath):
            os.mkdir(self.backupzpath)
        if not os.path.isdir(self.uzpath):
            os.mkdir(self.uzpath)
        if not os.path.isdir(self.jsonpath):
            os.mkdir(self.jsonpath)

    def unzip(self, period='month'):
        if 'month' == period: file = self.zmon
        elif 'all' == period: file = self.zall
        else: file = self.zmon
        with zipfile.ZipFile(os.path.join(self.zpath, file), 'r') as zf:
            zf.extractall(path=self.uzpath)
            # zipinfo = zf.infolist()
            # for zi in zipinfo:
            #     zi.filename = zi.filename.encode("cp437").decode("euc-kr")
            #     zf.extract(member=zi, path=self.uzpath)
            zf.close()

    def zip(self, period='month'):
        if 'month' == period: file = self.zmon
        elif 'all' == period: file = self.zall
        else: file = self.zmon
        with zipfile.ZipFile(os.path.join(self.zpath, file), 'w') as zf:
            root = self.uzpath
            for path, dir, files in os.walk(self.uzpath):
                for file in files:
                    fullpath = os.path.join(path, file)
                    relpath = os.path.relpath(fullpath, root)
                    zf.write(fullpath, relpath, zipfile.ZIP_DEFLATED)

zipper = Zipper()