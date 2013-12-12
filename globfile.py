__author__ = 'wanghuafeng'
#coding:utf-8
import glob
import os,shutil
from Readcsv import main
filepath= "C:\Users\Administrator\Desktop\data"#此处配置csv文件的存在目录
dirname = os.sep.join([filepath,"filebak"])

def glob_dir():
    dirpath = '\\'.join([filepath,'*.csv'])
    filelist = glob.glob(dirpath)#其返回的文件名只包括当前目录里的文件名，不包括子文件夹里的文件
    # print filepath
    for file in filelist:
        print file
        if os.path.exists(dirname):
            try:
                main(file)
            except EOFError:
                print 'file to db'
            shutil.move(file,dirname)
            print 'remove...'
        else:
            os.mkdir(dirname)
            main(file)
            print 'mkdiring...'
            shutil.move(file,dirname)
if __name__=="__main__":
    glob_dir()

