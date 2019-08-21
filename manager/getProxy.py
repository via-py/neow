# !/usr/bin/python3
# -*- coding: utf-8 -*-
"""
@Author         :  Zzmi
@Version        :
------------------------------------
@File           :  getProxy.py
@Description    :  从公网获取免费IP-proxy
@CreateTime     :  2019/8/19 16:56
------------------------------------
@ModifyTime     : 8.21 16:30
@ModifyContent  : 判断能否获取到IP来源信息，不能获取，则为暂无IP信息来源
"""
import sys
from pyquery import PyQuery as pq
from lxml import etree
from utils import RequestUtil


sys.path.append('..')


class ProxyMetaclass(type):
    def __new__(cls, name, bases, attrs):
        count = 0
        attrs['__CrawlFunc__'] = []
        for k, v in attrs.items():
            if 'crawl_' in k:
                attrs['__CrawlFunc__'].append(k)
                count += 1
        attrs['__CrawlFuncCount__'] = count
        return type.__new__(cls, name, bases, attrs)


class GetProxy(object, metaclass=ProxyMetaclass):

    def __init__(self):
        self.crawler = RequestUtil.RequestUtil()

    def get_proxies(self, callback):
        proxies = []
        for proxy in eval("self.{}()".format(callback)):
            print('成功获取到代理', proxy)
            proxies.append(proxy)
        return proxies

    def crawl_daili66(self):
        """
        代理66
        :param page_count: 页码
        :return: 代理
        """
        ip_dict = {}
        start_url = 'http://www.66ip.cn/{}.html'
        for i in range(1600, 1680):
            url = start_url.format(i)
            html = self.crawler.get(url=url)
            if html:
                doc = pq(html)
                infos = doc('.containerbox table tr:gt(0)').items()
                for info in infos:
                    ip = info.find('td:nth-child(1)').text()
                    port = info.find('td:nth-child(2)').text()
                    proxy_type = info.find('td:nth-child(4)').text()
                    address = info.find('td:nth-child(3)').text()
                    proxy_ip = ':'.join([ip, port])
                    ip_dict['proxy_type'] = proxy_type
                    ip_dict['address'] = address
                    ip_dict['proxy_ip'] = proxy_ip
                    yield ip, proxy_ip, proxy_type, address

    def crawl_ip3366(self):
        """
        云代理
        :return:
        """
        ip_dict = {}
        for i in range(1, 4):
            start_url = 'http://www.ip3366.net/?stype=1&page={}'.format(i)
            html = self.crawler.get(url=start_url)
            if html:
                doc = pq(html)
                infos = doc('#list tbody tr:gt(0)').items()
                # print(trs)
                for info in infos:
                    ip = info.find('td:nth-child(1)').text()
                    port = info.find('td:nth-child(2)').text()
                    proxy_type = info.find('td:nth-child(3)').text()
                    address = info.find('td:nth-child(6)').text()
                    proxy_ip = ':'.join([ip, port])
                    ip_dict['proxy_type'] = proxy_type
                    ip_dict['address'] = address
                    ip_dict['proxy_ip'] = proxy_ip
                    yield ip, proxy_ip, proxy_type, address

    def crawl_89ip(self):
        """
        89免费代理
        :return:
        """
        ip_dict = {}
        start_url = 'http://www.89ip.cn/'
        html = self.crawler.get(url=start_url)
        if html:
            doc = pq(html)
            infos = doc('.layui-table tbody tr:gt(0)').items()
            for info in infos:
                ip = info.find('td:nth-child(1)').text()
                port = info.find('td:nth-child(2)').text()
                proxy_type = info.find('td:nth-child(3)').text()
                address = info.find('td:nth-child(4)').text()
                proxy_ip = ':'.join([ip, port])
                ip_dict['proxy_type'] = proxy_type
                ip_dict['address'] = address
                ip_dict['proxy_ip'] = proxy_ip
                yield ip, proxy_ip, proxy_type, address

    def crawl_kxdaili(self):
        """
        开心代理
        :return:
        """
        ip_dict = {}
        for i in range(1, 11):
            start_url = 'http://www.kxdaili.com/dailiip/1/{}.html'.format(i)
            html = self.crawler.get(url=start_url)
            if html:
                doc = pq(html)
                infos = doc('.active tbody tr:gt(0)').items()
                for info in infos:
                    ip = info.find('td:nth-child(1)').text()
                    port = info.find('td:nth-child(2)').text()
                    proxy_type = info.find('td:nth-child(3)').text()
                    address = info.find('td:nth-child(6)').text()
                    proxy_ip = ':'.join([ip, port])
                    ip_dict['proxy_type'] = proxy_type
                    ip_dict['address'] = address
                    ip_dict['proxy_ip'] = proxy_ip
                    yield ip, proxy_ip, proxy_type, address


    def crawl_kuaidaili(self):
        """
        快代理
        :return:
        """
        ip_dict = {}
        for i in range(1, 4):
            start_url = 'http://www.kuaidaili.com/free/inha/{}/'.format(i)
            html = self.crawler.get(url=start_url)
            if html:
                doc = pq(html)
                infos = doc('#list tbody tr:gt(0)').items()
                print(infos)
                for info in infos:
                    ip = info.find('td:nth-child(1)').text()
                    port = info.find('td:nth-child(2)').text()
                    proxy_type = info.find('td:nth-child(5)').text()
                    address = info.find('td:nth-child(3)').text()
                    proxy_ip = ':'.join([ip, port])
                    ip_dict['proxy_type'] = proxy_type
                    ip_dict['address'] = address
                    ip_dict['proxy_ip'] = proxy_ip
                    yield ip, proxy_ip, proxy_type, address

    def crawl_xicidaili(self):
        """
        西刺代理
        :return:
        """
        ip_dict = {}
        for i in range(1, 3):
            start_url = 'http://www.xicidaili.com/nn/{}'.format(i)
            headers = {
                'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
                'Cookie': '_free_proxy_session=BAh7B0kiD3Nlc3Npb25faWQGOgZFVEkiJWRjYzc5MmM1MTBiMDMzYTUzNTZjNzA4NjBhNWRjZjliBjsAVEkiEF9jc3JmX3Rva2VuBjsARkkiMUp6S2tXT3g5a0FCT01ndzlmWWZqRVJNek1WanRuUDBCbTJUN21GMTBKd3M9BjsARg%3D%3D--2a69429cb2115c6a0cc9a86e0ebe2800c0d471b3',
                'Host': 'www.xicidaili.com',
                'Referer': 'http://www.xicidaili.com/nn/3',
                'Upgrade-Insecure-Requests': '1',
            }
            html = self.crawler.get(url=start_url, header=headers)
            etree_obj = etree.HTML(html)
            # 通过筛选response.content，得到包含ip信息的列表
            infos = etree_obj.xpath("//tr[@class='odd']")
            for info in infos:
                ip = info.xpath('./td[2]/text()')[0]
                port = info.xpath('./td[3]/text()')[0]
                proxy_type = info.xpath('.//td[@class="country"]/text()')[0]
                if info.xpath('./td[4]/a/text()'):
                    address = info.xpath('./td[4]/a/text()')
                else:
                    address = '暂无IP来源信息'
                proxy_ip = ':'.join([ip, port])
                ip_dict['proxy_type'] = proxy_type
                ip_dict['address'] = address
                ip_dict['proxy_ip'] = proxy_ip
                print(proxy_ip, proxy_type, address)
                #yield proxy_ip, proxy_type, address



