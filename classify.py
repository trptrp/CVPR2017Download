#!/usr/bin/env python
# coding=utf-8
import unicodedata
import time
from urllib import request
import re
from bs4 import BeautifulSoup
import shutil
from os import listdir
from os.path import isfile, join
def getHtml(url):
    page = request.urlopen(url)
    html = page.read()
    return html


def find_in_array(file_name_list,search_str):
    flag = 0
    index = 0
    search_str = unicodedata.normalize('NFKD', search_str).encode('ascii','ignore')
    for i in range(0,len(file_name_list)):
        if(not file_name_list[i].lower().find(search_str.lower())==-1):
            flag+=1
            index =i
    if flag == 1:
        return index
    else:
        return False


def mkdir(path):
    # 引入模块
    import os

    # 去除首位空格
    path=path.strip()
    # 去除尾部 \ 符号
    path=path.rstrip("\\")
    isExists=os.path.exists(path)

    # 判断结果
    if not isExists:
        # 如果不存在则创建目录
        # 创建目录操作函数
        os.makedirs(path)
        return True
    else:
        # 如果目录存在则不创建，并提示目录已存在
        return False
def letters(input):
    valids = []
    for character in input:
        if character.isalpha() or character == '-' or character.isdigit():
            valids.append(character)
    return ''.join(valids)

#file_path = '/home/sherwood/cvpr2016/'
#save_path = '/home/sherwood/cvpr2016_class/'
url = 'http://www.cvpapers.com/cvpr2017.html'
#files = [ f for f in listdir(file_path) if isfile(join(file_path,f)) ]
html = getHtml(url)
soup = BeautifulSoup(html, "lxml")
program_list = soup.find_all("dt")
count = 0
no_copy = 0
check = []
for i in range(0,len(program_list)):
    name = program_list[i].get_text()
    name_array = name.split(' ')

    name_array[0] = letters(name_array[0])
    ii = 1
    search_str = name_array[0]
    while ii <3 and ii < len(name_array):
        name_array[ii] = letters(name_array[ii])
        search_str = search_str + '_' + name_array[ii]
        ii = ii+1

    pre_h4 = program_list[i].find_previous("h4").text #
    pre_h3 = program_list[i].find_previous("h3").text # poster with 4-2 like tails or normal field

    #is Poster?
    partion = pre_h3.split(' ')
    if partion[0] == "Poster":
        paperClass = "Poster"
        field = pre_h4
    else:
        partion = pre_h4.split(' ')
        if partion[0] == "Spotlight":
            paperClass = "Spotlight"
        else:
            paperClass = "Oral"
        spacePose = pre_h3.rfind(' ')
        field = pre_h3[0:spacePose]
    print(paperClass + ' ' + field + ' ' + name)
#    dir_path = save_path+pre_h3+'/'+pre_h4+'/'
#     mkdir(dir_path)
#     index = find_in_array(files,search_str)
#     # if index in check:
#     #     print 'error'
#     #     print(index)
#     check.append(index)
#     if index:
#         shutil.copy(file_path+files[index],dir_path+files[index])
#         count += 1
#     else:
#         flag = 0
#         while (not index) and flag <3:
#             index = find_in_array(files,name_array[flag])
#             flag += 1
#         if index:
#             shutil.copy(file_path+files[index],dir_path+files[index])
#             count += 1
#         else:
#             shutil.copy(file_path+files[index],save_path+files[index])
#             no_copy += 1
#             count += 1
#             print(name)
#     #print "total is 643 and now is "+str(count)+"and no copy is"+str(no_copy)

print(len(program_list))

