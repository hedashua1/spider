import argparse
import requests
import multiprocessing
import html
from lxml import etree
import re
from threading import Thread
url_list = set()
catch_num = 0
default_layer = 3
thread_num = 0
num = 0
def spider(url = 'https://vip.iqiyi.com/?fv=zz_57b2d4c27f403-144878619-224842',keyword = '会员'):

    r = requests.get(url)
    if keyword in r.text:
        global url_list
        url_list.add(url)
        print('*'*50,len(url_list))
    temp = get_url(r.content)
    global default_layer
    default_layer -= 1
    if default_layer <= 0:
        return
    for i in temp:
        spider(i,keyword)


def get_url(content):
    tree = etree.HTML(content)
    contents = etree.tostring(tree)
    #转换为标准的html格式
    html_text = html.unescape(contents.decode('utf-8'))
    url_set = set()
    #通过正则表达获取url
    result = re.findall("http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\(\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+", html_text)
    for item in result:
        url_set.add(item)
        #print(item)
        global num
        num += 1
    return url_set



if __name__=="__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument('--u', type=str, default='', help="url")
    parser.add_argument('--d', type=int, default=1, help='deep')
    parser.add_argument('--log', type=str,default='spider.log', help="logfile path")
    parser.add_argument('--tn', type=int,default=1, help="threads_num")
    parser.add_argument('--key', type=str,default='', help="keyword")

    args = parser.parse_args()
   #global default_layer
   #default_layer = 3
    #global thread_num
    thread_num = 1

    spider()
    print('-'*50)
    print(url_list)
