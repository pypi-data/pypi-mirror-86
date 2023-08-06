import os
import time
import Common
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
            if e.__str__().find("404") != -1:
                print("[%s] 下载文件 \"%s\" [失败]，服务器不存在此文件。" % (time.ctime(), savename))
                return 1
            
            print("[%s] 第 %s 次下载文件 \"%s\" [失败]。剩余尝试次数： %s 。失败原因： %s" % (time.ctime(), str(attempts - remaining), savename, str(remaining), e))
            remaining -= 1
        else:
            print("[%s] 下载文件 \"%s\" [成功]，已保存到 \"%s\" 。" % (time.ctime(), savename, savepath))
            return 0
           
    print("[%s] 下载文件 \"%s\" [失败]，尝试次数用尽。" % (time.ctime(), savename))
    
    if os.path.exists(savepath + savename):
        os.remove(savepath + savename)
    
    return 1

'''def MultiThreadsDownload(url: str, savepath: str = None,savename: str = None, attempts: int = 5, createdir: bool = True, Threads: int = 4):
    """
    因为用不了requests库，所以立即下载文件。
    当遇到大文件这样做时，文件将被立即下载。
    并且文件特别大时且内存不够，可能会报错。
    我们目前没有办法，解决办法还在讨论之中。
    如果有想法，欢迎在lazytool.py提issue。
    十分十分十分十分十分十分十分十分谢谢！
    """
    return 1
    #it's skip...'''