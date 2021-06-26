import zipfile
import os


class Zipper:
    def __init__(self):
        self.root = 'C:/임시/_KDATA'
        self.zpath = 'C:/임시/_KDATA/kZipfile/zip'
        self.uzpath = 'C:/임시/_KDATA/kZipfile/unzip'
        self.jsonpath = 'C:/임시/_KDATA/kZipfile/localdata_json'
        self.zall = 'LOCALDATA_ALL_XML.zip'
        self.zmon = 'LOCALDATA_NOWMON_XML.zip'

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