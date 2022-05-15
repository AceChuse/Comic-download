# -*- coding: utf-8 -*-
import requests
import os
from bs4 import BeautifulSoup
from manhua_python.js_back import Mangabz



def Download(URL, title):
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/89.0.4381.8 Safari/537.36'
    }

    r = requests.get(URL, headers=headers, stream=True)
    img_name_start = URL.rfind("/")
    img_name_end = len(URL)
    img_name = URL[img_name_start + 1:img_name_end]
    if r.status_code == 200:
        print("正在下载:" + img_name)
        isExists = os.path.exists(DIR + title)
        if not isExists:
            os.makedirs(DIR + title)
            print("已创建" + DIR + title)
        open(DIR + title + '/' + img_name, 'wb').write(r.content)  # 将内容写入图片
        print("下载完成")
    else:
        raise ValueError("status_code={status_code}".format(status_code=r.status_code))
    del r

# 無職轉生
# DEF_DIR = "E:/漫画/無職轉生/"
# comic_url = "http://www.mangabz.com/1864bz/"

# 藍色的除魔師
DEF_DIR = "E:/漫画/藍色的除魔師/"
comic_url = "http://www.mangabz.com/21bz/"

# 人形之國APOSIMZ
# DEF_DIR = "E:/漫画/人形之國APOSIMZ/"
# comic_url = "http://www.mangabz.com/92bz/"


START_CHAPTER_CODE = "0"
START_PAGE = 1
if (0 == 0):
    START_CHAPTER = input("请输入从倒数第几章开始(默认从最新的章节开始)：")
    if START_CHAPTER != "":
        START_CHAPTER = int(START_CHAPTER) - 1
    else:
        START_CHAPTER = 0
    START_PAGE = input("请输入从第几页开始(默认从第一页开始)：")
    if START_PAGE == "":
        START_PAGE = 1
    DIR = input("请输入保存路径(默认" + DEF_DIR + ")：")
    if DIR == "":
        DIR = DEF_DIR
    print("操作成功！正在准备开始")
    s11 = START_CHAPTER + 1
    # 开始获取章节列表
    doc = requests.get(comic_url)
    html = doc.text
    bf = BeautifulSoup(html, features="html.parser")
    texts = bf.find_all('a', class_='detail-list-form-item')
    texts_num = len(texts)
    for i in range(texts_num - START_CHAPTER - 1,  -1, -1):
    # for i in range(START_CHAPTER, texts_num):
        html = texts[i]
        html = str(html)
        # 获取章节代码
        # print(html)
        chapter_string = "href=\"/m"
        chapter_num = len(chapter_string)
        chapter_int = int(html.find(chapter_string))
        chapter_end = int(html.find("/", chapter_int + chapter_num))
        chapter_code = html[chapter_int + chapter_num:chapter_end]
        if i == START_CHAPTER:
            START_CHAPTER_CODE = chapter_code
        # 获取标题
        title_string = "\">"
        title_num = len(title_string)
        title_int = int(html.find(title_string))
        title_end = int(html.find("<", title_int + title_num))
        title = html[title_int + title_num:title_end]
        title = title.rstrip()
        print("正在获取->章节代码：" + chapter_code + " 标题：" + title)

        Mangabz("http://www.mangabz.com/m" + chapter_code + "/").run(DIR=DIR, title=title)
