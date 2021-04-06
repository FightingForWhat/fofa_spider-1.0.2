# -*- coding: utf-8 -*-
# !/usr/bin/python
# @Time    : 2021-04-06
# @Author  : 409162075
# @FileName: fofa_spider.py
# version: 1.0.2

import requests
import base64
import re
import config
import random
from urllib.parse import quote


def logo():
    print(r'''
  _____       _____                        .__    .___            
_/ ____\_____/ ____\____      ____________ |__| __| _/___________ 
\   __\/  _ \   __\\__  \    /  ___/\____ \|  |/ __ |/ __ \_  __ \
 |  | (  <_> )  |   / __ \_  \___ \ |  |_> >  / /_/ \  ___/|  | \/
 |__|  \____/|__|  (____  / /____  >|   __/|__\____ |\___  >__|   
                        \/       \/ |__|           \/    \/       
                                                    version 1.0.2
    ''')


def check_cookie():
    if config.fofa_token == "":
        print("[*] 请配置config fofa_token文件")
        exit(0)
    print("[*] 检测到fafa_token，请保证token可用")
    return


def headers():
    user_agent_use = config.user_agent[random.randint(0, len(config.user_agent) - 1)]
    headers_use = {
        'User-Agent': user_agent_use,
        'Accept': 'application/json, text/plain, */*',
        'Authorization': config.fofa_token
    }
    return headers_use


def search_key_input():
    search_key = input('[*] 请输入fofa搜索关键字: ')
    search_key = '\"' + search_key + '\"'
    return search_key


def get_page_num(search_key):
    headers_use = headers()
    searchbs64 = quote(str(base64.b64encode(search_key.encode()), encoding='utf-8'))

    print("[*] 爬取页面为:https://fofa.so/result?&qbase64=" + searchbs64)
    html = requests.get(url="https://fofa.so/result?&qbase64=" + searchbs64, headers=headers_use).text
    pagenum = re.findall('<li class="number">(\d*)</li></ul><button type="button" class="btn-next">', html)
    print("[*] 该关键字存在页码: " + pagenum[0] + '页')
    return searchbs64, headers_use


def fofa_spider_page(page, searchurl, searchbs64, headers_use):
    print("[*] 正在爬取第" + str(page) + "页" + '\n')
    request_url = 'https://api.fofa.so/v1/search?q=' + searchurl + '&qbase64=' + searchbs64 + '&full=false&pn=' + str(page) + '&ps=10'
    page_json = requests.get(request_url, headers=headers_use).json()
    page_data = page_json['data']['assets']
    # print(type(page_json))
    # print(page_json.keys())
    doc_result = open('fofa_result.txt', 'a+')
    for i in range(len(page_data)):
        host_data = page_data[i]['link']
        doc_result.write(host_data + '\n')
        # html_time = page_data[i]['mtime']
        print('[+] ' + host_data)
    print()
    print("[*] 第" + str(page) + "页爬取完毕 爬取数据" + str(i + 1) + '条\n')
    doc_result.close()
    return


def fofa_spider(search_key, searchbs64, headers_use):
    searchurl = quote(search_key)
    start_page = input("[*] 请输入开始页码: ")
    stop_page = input("[*] 请输入终止页码: ")
    print()
    # doc = open("hello_world.txt", "a+")
    for page in range(int(start_page), int(stop_page) + 1):
        fofa_spider_page(page, searchurl, searchbs64, headers_use)

    return


def main():
    logo()
    check_cookie()
    search_key = search_key_input()
    searchbs64, headers_use = get_page_num(search_key)
    fofa_spider(search_key, searchbs64, headers_use)

    return


if __name__ == '__main__':
    main()
