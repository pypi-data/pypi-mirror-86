import os
import time
from .common import common
import urllib.error, urllib.request

class Download(object):
    """
    Download file part of lazytool.py
    """
    def __init__(self):
        pass
    
    def fileDownload(url: str, savepath: str = None,savename: str = None, attempts: int = 5, createdir: bool = True):
        remaining = attempts - 1
        if savepath == None:
            savepath = ".{0}Download{0}".format(os.sep)
        
        if savename == None:
            savename = url.split("/")[-1]
        
        if not os.path.exists(savepath) and createdir:
            os.makedirs(savepath)
        
        if not url.split("/")[0] in common.RequestHeaders:
            print("fileDownload(): 传入的链接无效。")
            return 1
        
        if len(os.sep) == 2:
            if not savepath[-1:] == os.sep:
                print("fileDownload()：传入的保存地址无效（应以\"\\\\\"结束）。")
                return 1
        elif len(os.sep) == 1:
            if not savepath[-1] == os.sep:
                print("fileDownload()：传入的保存地址无效（应以\"/\"结束）。")
                return 1
        
        print("[%s] 开始下载在 %s 上的文件 \"%s\" 。" % (time.ctime(), url.split("/")[2], savename))
        while not remaining < 0:
        
            try:
                urllib.request.urlretrieve(url, savepath + savename)
            except urllib.error.URLError as e:
                print("[%s] 第 %s 次下载文件 \"%s\" [失败]。剩余尝试次数： %s 。失败原因： %s" % (time.ctime(), str(attempts - remaining), savename, str(remaining), e))
                remaining -= 1
            else:
                print("[%s] 下载文件 \"%s\" [成功]，已保存到 \"%s\" 。" % (time.ctime(), savename, savepath))
                return 0
            
        print("[%s] 下载文件 \"%s\" [失败]，尝试次数用尽。" % (time.ctime(), savename))
        
        if os.path.exists(savepath + savename):
            os.remove(savepath + savename)
        
        return 1

        