#!/usr/bin/env python3
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
        if(not bytes(file_name_list[i].lower(), 'utf-8').find(search_str.lower())==-1):
            flag+=1
            index =i
    if flag == 1:
        return index
    else:
        return False


def mkdir(path):
    import os

    path=path.strip()
    path=path.rstrip("\\")
    isExists=os.path.exists(path)
    if not isExists:
        os.makedirs(path)
        return True
    else:
        return False

def letters(input):
    valids = []
    for character in input:
        if character.isalpha() or character == '-' or character.isdigit():
            valids.append(character)
    return ''.join(valids)


file_path = '/Users/trp/cvpr2017/'
save_path = '/Users/trp/cvpr2017_class/'
url = 'http://www.cvpapers.com/cvpr2017.html'
files = [ f for f in listdir(file_path) if isfile(join(file_path,f)) ]
html = getHtml(url)
soup = BeautifulSoup(html, "html.parser")
program_list = soup.find_all("dt")
count = 0 
no_copy = 0
check = []
error_item = []
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
    try:
        print(paperClass + ' ' + field + '/' + name)
    except:
        error_item.append(name)
        continue
    dir_path = save_path+paperClass+'/'+field+'/'
    mkdir(dir_path)
    index = find_in_array(files,search_str)
    if index in check:
        print('error')
        print(index)
    check.append(index)
    if index:
        shutil.copy(file_path+files[index],dir_path+files[index])
        count += 1
    else:
        flag = 0
        while (not index) and flag <3:
            index = find_in_array(files,name_array[flag])
            flag += 1
        if index:
            shutil.copy(file_path+files[index],dir_path+files[index])
            count += 1
        else:
            shutil.copy(file_path+files[index],save_path+files[index])
            no_copy += 1
            count += 1
            print(name)

print(len(error_item))
for item in error_item:
    print(item.encode('utf-8'))
print(len(check))
print(len(program_list))

