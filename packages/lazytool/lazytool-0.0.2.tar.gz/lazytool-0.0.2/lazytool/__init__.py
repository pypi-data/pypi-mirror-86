import os

from .Download import *
if not "IMPORT_ALL_IS_A_JOKE" in os.environ:
    print("lazytool: Bro, import ALL is a joke, right?")

if __name__ == '__main__':
    Download.fileDownload("https://raw.fastgit.org/HelloGwkki/test/main/test")