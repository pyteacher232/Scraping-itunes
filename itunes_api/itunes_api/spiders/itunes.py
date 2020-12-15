# -*- coding: utf-8 -*-
import scrapy
from scrapy.http import FormRequest
from scrapy.selector import HtmlXPathSelector
from string import ascii_uppercase
import re
import xml.etree.ElementTree as ET
from bs4 import BeautifulSoup
import json
import random
import requests

proxy_file_name = 'proxy_http_ip.txt'
PROXIES = []
with open(proxy_file_name, 'rb') as text:
    PROXIES = ["http://" + x.decode("utf-8").strip() for x in text.readlines()]

class ItunesSpider(scrapy.Spider):
    name = 'itunes'
    allowed_domains = []
    start_urls = []

    def __init__(self):
        self.total_cnt = 0
        self.create_result_file(result_file_name='itunes_result.csv')


    def start_requests(self):

        # for i in range(73329241, 1446290715)
        for i in range(50000000, 2000000000, 200):
            id_list = [str(j) for j in range(i, i+200)]
            query = ','.join(id_list)
            API = 'https://itunes.apple.com/lookup?media=podcast&entity=podcast&id={}'.format(query)

            print_txt = "[Start ID] {}".format(i)
            print(print_txt)

            pxy = random.choice(PROXIES)
            request = FormRequest(
                url=API,
                method="GET",
                callback=self.parse,
                meta={
                    'proxy': pxy
                }
            )

            yield request

    def parse(self, response):
        json_parsed = json.loads(response.text)
        results = json_parsed['results']
        if results:
            for result in results:
                try:
                    title = result['collectionName']
                except:
                    title = ''
                try:
                    author = result['artistName']
                except:
                    author = ''
                try:
                    itunes_url = result['collectionViewUrl']
                except:
                    itunes_url = ''
                try:
                    rss_feed = result['feedUrl']
                except:
                    rss_feed = ''
                try:
                    kind = result['kind']
                except:
                    kind = ''
                if kind != 'podcast':
                    continue
                result = [title, author, itunes_url, rss_feed]
                if rss_feed:
                    headers = {
                        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.110 Safari/537.36',
                    }

                    pxy = random.choice(PROXIES)

                    request = FormRequest(
                        url=rss_feed,
                        headers=headers,
                        method="GET",
                        callback=self.get_email,
                        meta={
                            'result': result,
                            'handle_httpstatus_all': True,
                            'dont_redirect': True,
                            'proxy': pxy
                        }
                    )

                    yield request
                else:
                    self.insert_row(result_row=result)
                    self.total_cnt += 1
                    print_txt = "[Details {}] {}".format(self.total_cnt, result)
                    print(print_txt)

    def get_email(self, response):

        result = response.meta['result']
        soup = BeautifulSoup(response.text, 'lxml')

        try:
            email = soup.find('itunes:email').text
        except:
            email = ''

        result_row = result + [email]
        self.insert_row(result_row=result_row)
        self.total_cnt += 1
        print_txt = "[Details {}] {}".format(self.total_cnt, result_row)
        print(print_txt)

    def create_result_file(self, result_file_name):
        heading = [
            "Title", "Author", "itunes URL", "RSS Feed", "Email"
        ]

        import codecs
        self.result_file = codecs.open(result_file_name, "w", "utf-8")
        self.result_file.write(u'\ufeff')
        self.insert_row(result_row=heading)

    def insert_row(self, result_row):
        self.result_file.write('"' + '","'.join(result_row) + '"' + "\n")
        self.result_file.flush()
'''
scrapy crawl itunes -s LOG_ENABLED=False
'''

if __name__ == '__main__':
    from scrapy.utils.project import get_project_settings
    from scrapy.crawler import CrawlerProcess, CrawlerRunner

    settings = get_project_settings()
    process = CrawlerProcess(settings)
    process.crawl(ItunesSpider)
    process.start()
