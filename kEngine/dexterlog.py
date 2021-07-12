import logging.handlers
import os
import datetime
from kSecret import config

'''
logging.DEBUG   : win32evtlog.EVENTLOG_INFORMATION_TYPE,
logging.INFO    : win32evtlog.EVENTLOG_INFORMATION_TYPE,
logging.WARNING : win32evtlog.EVENTLOG_WARNING_TYPE,
logging.ERROR   : win32evtlog.EVENTLOG_ERROR_TYPE,
logging.CRITICAL: win32evtlog.EVENTLOG_ERROR_TYPE,
'''

def createfolder(path):
    if not os.path.exists(path):
        os.makedirs(path)

def createfile(foldername, filename):
    now = datetime.datetime.now()
    nowtuple = now.timetuple()
    createfolder(foldername)
    foldername = foldername + str(nowtuple.tm_year) + '/'
    createfolder(foldername)
    foldername = foldername + str(nowtuple.tm_mon) + '/'
    createfolder(foldername)
    foldername = foldername + str(nowtuple.tm_mday) + '/'
    createfolder(foldername)
    logfile = foldername + filename + '.log'
    return logfile

def klogger(filename):
    # 초기화
    foldername = config.config['root'] + 'kLog/'
    looooger = logging.getLogger(filename)
    looooger.setLevel(logging.DEBUG)

    # 핸들러 리셋
    for hdlr in looooger.handlers[:]:  # remove all old handlers
        looooger.removeHandler(hdlr)

    # 일자별 폴더 생성
    logfile = createfile(foldername, filename)

    # 핸들러 설정
    logfomatter = logging.Formatter('%(asctime)s   [%(levelname)s|%(filename)s:%(lineno)s] > %(message)s')
    logfilemaxbyte = 1024 * 1024 * 100 # 100MB
    logfilehandler = logging.handlers.RotatingFileHandler(logfile, maxBytes=logfilemaxbyte, backupCount=10)
    logstreamhandler = logging.StreamHandler()
    logfilehandler.setFormatter(logfomatter)
    logstreamhandler.setFormatter(logfomatter)
    looooger.addHandler(logfilehandler)
    looooger.addHandler(logstreamhandler)

    return looooger
