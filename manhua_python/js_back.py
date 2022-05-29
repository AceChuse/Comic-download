
# 代码解释原文： https://blog.csdn.net/weixin_40352715/article/details/106588609

import re
import execjs
import requests
import urllib.parse

import os
import time



def Download(URL, DIR, title, page):
    headers = {
        "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_4) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/81.0.4044.138 Safari/537.36",
        "Referer": URL,
        "Cookie": "image_time_cookie=17115|637270678077155170|2",
    }

    max_try = 12
    for i in range(max_try):
        try:
            r = requests.get(URL, headers=headers, stream=True, timeout=20)
            break
        except Exception as exc:
            if i + 1 < max_try:
                print(exc)
                time.sleep(2)
            else:
                raise ValueError(exc)

    # while 1:
    #     try:
    #         r = requests.get(URL, headers=headers, stream=True, timeout=20)
    #         break
    #     except Exception as exc:
    #         print(exc)
    #         time.sleep(5)

    img_name_start = URL.rfind("/")
    img_name_end = len(URL)
    img_name = URL[img_name_start + 1:img_name_end]
    if r.status_code == 200:
        print("正在下载:" + img_name)
        isExists = os.path.exists(DIR + title)
        if not isExists:
            os.makedirs(DIR + title)
            print("已创建" + DIR + title)
        open(DIR + title + '/' + str(page) + '.jpg', 'wb').write(r.content)  # 将内容写入图片
        print("下载完成")
    else:
        raise ValueError("status_code={status_code}".format(status_code=r.status_code))
    del r

class Mangabz:
    """
    日本漫画漫画章节图片下载
    """
    def __init__(self, url):
        self.url = url
        self.max_try = 12
        self.session = requests.Session()
        self.headers = {"User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_4) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/81.0.4044.138 Safari/537.36",
                        "Referer": self.url,
                        "Cookie": "image_time_cookie=17115|637270678077155170|2",
                        }

    def get_chapter_argv(self):
        print('url', self.url)

        for i in range(self.max_try):
            try:
                res = requests.get(self.url, headers=self.headers, timeout=20)
                break
            except Exception as exc:
                if i + 1 < self.max_try:
                    print(exc)
                    time.sleep(2)
                else:
                    raise ValueError(exc)


        mangabz_cid = re.findall("MANGABZ_CID=(.*?);", res.text)[0]
        mangabz_mid = re.findall("MANGABZ_MID=(.*?);", res.text)[0]
        page_total = re.findall("MANGABZ_IMAGE_COUNT=(.*?);", res.text)[0]
        mangabz_viewsign_dt = re.findall("MANGABZ_VIEWSIGN_DT=\"(.*?)\";", res.text)[0]
        mangabz_viewsign = re.findall("MANGABZ_VIEWSIGN=\"(.*?)\";", res.text)[0]
        return (mangabz_cid, mangabz_mid, mangabz_viewsign_dt, mangabz_viewsign, page_total)

    def get_images_js(self, page, mangabz_cid, mangabz_mid, mangabz_viewsign_dt, mangabz_viewsign):
        url = self.url + "chapterimage.ashx?" + "cid=%s&page=%s&key=&_cid=%s&_mid=%s&_dt=%s&_sign=%s" % (mangabz_cid, page, mangabz_cid, mangabz_mid, urllib.parse.quote(mangabz_viewsign_dt), mangabz_viewsign)
        res = self.session.get(url, headers=self.headers, timeout=10)
        self.headers["Referer"] = res.url
        return res.text

    def run(self, DIR, title):
        mangabz_cid, mangabz_mid, mangabz_viewsign_dt, mangabz_viewsign, page_total = self.get_chapter_argv()


        for page in range(1, int(page_total) + 1):

            for i in range(self.max_try):
                try:
                    js_str = self.get_images_js(page, mangabz_cid, mangabz_mid, mangabz_viewsign_dt, mangabz_viewsign)
                    imagesList = execjs.eval(js_str)
                    print(imagesList[0])

                    Download(imagesList[0], DIR, title, page)
                    break
                except Exception as exc:
                    if i + 1 < self.max_try:
                        print(exc)
                        time.sleep(2)
                    else:
                        raise ValueError(exc)




if __name__ == '__main__':
    mangabz = Mangabz("http://www.mangabz.com/m17115/")
    # mangabz = Mangabz("http://www.mangabz.com/m11487/", )
    mangabz.run(DIR="E:/漫画/", title='test')
"""
result:
http://image.mangabz.com/1/249/17115/1_9913.jpg?cid=17115&key=16f4cd6d4bc919191eb29b37a2bcf872&uk=
http://image.mangabz.com/1/249/17115/2_3245.jpg?cid=17115&key=eb6e23a95153bbd5efe6ca81ea3016f6&uk=
http://image.mangabz.com/1/249/17115/3_6479.jpg?cid=17115&key=eb6e23a95153bbd5efe6ca81ea3016f6&uk=
http://image.mangabz.com/1/249/17115/4_5401.jpg?cid=17115&key=eb6e23a95153bbd5efe6ca81ea3016f6&uk=
http://image.mangabz.com/1/249/17115/5_3441.jpg?cid=17115&key=eb6e23a95153bbd5efe6ca81ea3016f6&uk=
http://image.mangabz.com/1/249/17115/6_9421.jpg?cid=17115&key=eb6e23a95153bbd5efe6ca81ea3016f6&uk=
http://image.mangabz.com/1/249/17115/7_3221.jpg?cid=17115&key=eb6e23a95153bbd5efe6ca81ea3016f6&uk=
http://image.mangabz.com/1/249/17115/8_3533.jpg?cid=17115&key=eb6e23a95153bbd5efe6ca81ea3016f6&uk=
http://image.mangabz.com/1/249/17115/9_4780.jpg?cid=17115&key=eb6e23a95153bbd5efe6ca81ea3016f6&uk=
http://image.mangabz.com/1/249/17115/10_2250.jpg?cid=17115&key=eb6e23a95153bbd5efe6ca81ea3016f6&uk=
http://image.mangabz.com/1/249/17115/11_3742.jpg?cid=17115&key=eb6e23a95153bbd5efe6ca81ea3016f6&uk=
http://image.mangabz.com/1/249/17115/12_6481.jpg?cid=17115&key=eb6e23a95153bbd5efe6ca81ea3016f6&uk=
http://image.mangabz.com/1/249/17115/13_4772.jpg?cid=17115&key=eb6e23a95153bbd5efe6ca81ea3016f6&uk=
http://image.mangabz.com/1/249/17115/14_1675.jpg?cid=17115&key=eb6e23a95153bbd5efe6ca81ea3016f6&uk=
http://image.mangabz.com/1/249/17115/15_1266.jpg?cid=17115&key=eb6e23a95153bbd5efe6ca81ea3016f6&uk=
http://image.mangabz.com/1/249/17115/16_9599.jpg?cid=17115&key=eb6e23a95153bbd5efe6ca81ea3016f6&uk=
http://image.mangabz.com/1/249/17115/17_4840.jpg?cid=17115&key=eb6e23a95153bbd5efe6ca81ea3016f6&uk=
http://image.mangabz.com/1/249/17115/18_5913.jpg?cid=17115&key=eb6e23a95153bbd5efe6ca81ea3016f6&uk=
http://image.mangabz.com/1/249/17115/19_1302.jpg?cid=17115&key=eb6e23a95153bbd5efe6ca81ea3016f6&uk=
http://image.mangabz.com/1/249/17115/20_6355.jpg?cid=17115&key=eb6e23a95153bbd5efe6ca81ea3016f6&uk=
http://image.mangabz.com/1/249/17115/21_3462.jpg?cid=17115&key=eb6e23a95153bbd5efe6ca81ea3016f6&uk=
http://image.mangabz.com/1/249/17115/22_6553.jpg?cid=17115&key=eb6e23a95153bbd5efe6ca81ea3016f6&uk=
http://image.mangabz.com/1/249/17115/23_5102.jpg?cid=17115&key=eb6e23a95153bbd5efe6ca81ea3016f6&uk=

关于图片下载可以看我其他的爬虫文章
"""
