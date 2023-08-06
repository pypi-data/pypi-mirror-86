import os

import Download
import common
if not "IMPORT_ALL_IS_A_JOKE" in os.environ:
    print("lazytool: Bro, import ALL is a joke, right?")

if __name__ == '__main__':
    print(common.RandomUA())
    Download.fileDownload("https://raw.fastgit.org/HelloGwkki/test/main/test")