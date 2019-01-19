# -*- coding:utf-8 -*-
import scrapy

class ShiyanlouSpider(scrapy.Spider):
    name = 'github-repositories'

    @property
    def start_urls(self):
        url_tmpl='https://github.com/shiyanlou?page={}&tab=repositories'
        return (url_tmpl.format(i) for i in range(1,5))

    def parse(self,response):
        for repository in response.xpath('.//div[@id="user-repositories-list"]/ul[@data-filterable-for="your-repos-filter"]/li'):
            yield {
                'name': repository.xpath('.//a[@itemprop="name codeRepository"]/text()').re_first('[\w\-\_]+'),
                'update_time': repository.xpath('.//div[@class="f6 text-gray mt-2"]/relative-time/@datetime').extract_first(default='Missing')
            }
