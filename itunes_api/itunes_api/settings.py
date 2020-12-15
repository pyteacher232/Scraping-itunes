# -*- coding: utf-8 -*-

# Scrapy settings for itunes_api project
#
# For simplicity, this file contains only settings considered important or
# commonly used. You can find more settings consulting the documentation:
#
#     https://doc.scrapy.org/en/latest/topics/settings.html
#     https://doc.scrapy.org/en/latest/topics/downloader-middleware.html
#     https://doc.scrapy.org/en/latest/topics/spider-middleware.html

BOT_NAME = 'itunes_api'

SPIDER_MODULES = ['itunes_api.spiders']
NEWSPIDER_MODULE = 'itunes_api.spiders'


# Crawl responsibly by identifying yourself (and your website) on the user-agent
#USER_AGENT = 'itunes_api (+http://www.yourdomain.com)'

# Obey robots.txt rules
ROBOTSTXT_OBEY = False


CONCURRENT_REQUESTS = 10
RETRY_TIMES = 10
DOWNLOAD_TIMEOUT = 100