# -*- coding: UTF-8 -*-
'''
---------------

Description of this file

:author: Luopeng
:date created: 2019-08-19
:python version: 3.6

---------------
'''
import requests
from requests.exceptions import ConnectionError
from pyquery import PyQuery as pq
from lxml import etree


base_headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/54.0.2840.71 Safari/537.36',
    'Accept-Encoding': 'gzip, deflate, sdch',
    'Accept-Language': 'en-US,en;q=0.9,zh-CN;q=0.8,zh;q=0.7',
    'content-type': 'charset=utf8'
}


def get_page(url, options={}):
    """
    抓取代理
    :param url:
    :param options:
    :return:
    """
    headers = dict(base_headers, **options)
    print('正在抓取', url)
    try:
        response = requests.get(url, headers=headers)
        print('抓取成功', url, response.status_code)
        if response.status_code == 200:
            return response.content #使用response.text的时候会出现乱码的问题
    except ConnectionError:
        print('抓取失败', url)
        return None


def crawl_daili66():
    """
    代理66
    :param page_count: 页码
    :return: 代理
    """

    start_url = 'http://www.66ip.cn/{}.html'
    for i in range(1600, 1680):
        url = start_url.format(i)
        html = get_page(url)
        if html:
            doc = pq(html)
            infos = doc('.containerbox table tr:gt(0)').items()
            for info in infos:
                ip = info.find('td:nth-child(1)').text()
                port = info.find('td:nth-child(2)').text()
                proxy_type = info.find('td:nth-child(4)').text()
                address = info.find('td:nth-child(3)').text()
                #print(ip, port, address, proxy_type)
                return ':'.join([ip, port]), address, proxy_type


def crawl_ip3366():
    """
    云代理
    :return:
    """
    for i in range(1, 4):
        start_url = 'http://www.ip3366.net/?stype=1&page={}'.format(i)
        html = get_page(start_url)
        if html:
            doc = pq(html)
            infos = doc('#list tbody tr:gt(0)').items()
            #print(trs)
            for info in infos:
                ip = info.find('td:nth-child(1)').text()
                port = info.find('td:nth-child(2)').text()
                proxy_type = info.find('td:nth-child(3)').text()
                address = info.find('td:nth-child(6)').text()
                #print(ip, port, proxy_type, address)
                return ':'.join([ip, port]), address, proxy_type


def crawl_89ip():
    """
    89免费代理
    :return:
    """
    start_url = 'http://www.89ip.cn/'
    html = get_page(start_url)
    if html:
        doc = pq(html)
        infos = doc('.layui-table tbody tr:gt(0)').items()
        for info in infos:
            ip = info.find('td:nth-child(1)').text()
            port = info.find('td:nth-child(2)').text()
            proxy_type = info.find('td:nth-child(3)').text()
            address = info.find('td:nth-child(4)').text()
            #print(ip, port, proxy_type, address)
            return ':'.join([ip, port]), address, proxy_type


def crawl_kxdaili():
    """
    开心代理
    :return:
    """
    for i in range(1, 11):
        start_url = 'http://www.kxdaili.com/dailiip/1/{}.html'.format(i)
        html = get_page(start_url)
        if html:
            doc = pq(html)
            infos = doc('.active tbody tr:gt(0)').items()
            for info in infos:
                ip = info.find('td:nth-child(1)').text()
                port = info.find('td:nth-child(2)').text()
                proxy_type = info.find('td:nth-child(3)').text()
                address = info.find('td:nth-child(6)').text()
                #print(ip, port, proxy_type, address)
                return ':'.join([ip, port]), address, proxy_type


def crawl_kuaidaili():
    """
    快代理
    :return:
    """
    for i in range(1, 4):
        start_url = 'http://www.kuaidaili.com/free/inha/{}/'.format(i)
        html = get_page(start_url)
        if html:
            doc = pq(html)
            infos = doc('#list tbody tr:gt(0)').items()
            print(infos)
            for info in infos:
                ip = info.find('td:nth-child(1)').text()
                port = info.find('td:nth-child(2)').text()
                proxy_type = info.find('td:nth-child(5)').text()
                address = info.find('td:nth-child(3)').text()
                #print(ip, port, proxy_type, address)
                return ':'.join([ip, port]), address, proxy_type


def crawl_xicidaili():
    for i in range(1, 3):
        start_url = 'http://www.xicidaili.com/nn/{}'.format(i)
        headers = {
            'Accept':'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
            'Cookie':'_free_proxy_session=BAh7B0kiD3Nlc3Npb25faWQGOgZFVEkiJWRjYzc5MmM1MTBiMDMzYTUzNTZjNzA4NjBhNWRjZjliBjsAVEkiEF9jc3JmX3Rva2VuBjsARkkiMUp6S2tXT3g5a0FCT01ndzlmWWZqRVJNek1WanRuUDBCbTJUN21GMTBKd3M9BjsARg%3D%3D--2a69429cb2115c6a0cc9a86e0ebe2800c0d471b3',
            'Host':'www.xicidaili.com',
            'Referer':'http://www.xicidaili.com/nn/3',
            'Upgrade-Insecure-Requests':'1',
        }
        html = get_page(start_url, options=headers)
        etree_obj = etree.HTML(html)
        # 通过筛选response.content，得到包含ip信息的列表
        infos = etree_obj.xpath("//tr[@class='odd']")
        for info in infos:
            ip = info.xpath('./td[2]/text()')[0]
            port = info.xpath('./td[3]/text()')[0]
            proxy_type = info.xpath('.//td[@class="country"]/text()')[0]
            address = info.xpath('./td[4]/a/text()')[0]
            #print(ip, port, address, proxy_type)
            return ':'.join([ip, port]), address, proxy_type


if __name__ == '__main__':
    crawl_xicidaili()