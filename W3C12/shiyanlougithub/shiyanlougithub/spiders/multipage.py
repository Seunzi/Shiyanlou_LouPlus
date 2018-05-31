# -*- coding: utf-8 -*-
import scrapy
from shiyanlougithub.items import ShiyanlougithubItem

class MultipageSpider(scrapy.Spider):
    name = 'multipage'
    
    @property
    def start_urls(self):
        return ('https://github.com/shiyanlou?page={}&tab=repositories'.format(i) for i in range(1,5))

    def parse(self, response):
        for repository in response.xpath('.//div[@id="user-repositories-list"]/ul[@    data-filterable-for="your-repos-filter"]/li'):
            item = ShiyanlougithubItem()
            item['name'] = repository.xpath('.//a[@itemprop="name codeRepository"]/text()').re_first('[\w\-\_]+')
            item['update_time'] = repository.xpath('.//div[@class="f6 text-gray mt-2"]/relative-time/@datetime').extract_first(default='Missing')

            detail_url = response.urljoin(repository.xpath('.//a[@itemprop="name codeRepository"]/@href').extract_first()
            request = scrapy.Request(detail_url,callback=self.parse_details)
            request.meta['item'] = item
            yield request

    def parse_details(self,response):
        item = response.meta['item']

        item['commits'] = response.xpath('.//div[@class="stats-switcher-wrapper"]/ul[@class="numbers-summary"]/li[1]/a/span/text()').re_first('[^\d]*(\d*)[^\d*]')
        item['branches'] = response.xpath('.//div[@class="stats-switcher-wrapper"]/ul[@class="numbers-summary"]/li[2]/a/span/text()').re_first('[^\d]*(\d*)[^\d*]')
        item['releases'] = response.xpath('.//div[@class="stats-switcher-wrapper"]/ul[@class="numbers-summary"]/li[3]/a/span/text()').re_first('[^\d]*(\d*)[^\d*]')

        yield item
