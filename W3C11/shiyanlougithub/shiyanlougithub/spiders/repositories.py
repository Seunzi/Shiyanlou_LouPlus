# -*- coding: utf-8 -*-
import scrapy
from shiyanlougithub.items import ShiyanlougithubItem

class RepositoriesSpider(scrapy.Spider):
    name = 'repositories'

    @property
    def start_urls(self):
        return ('https://github.com/shiyanlou?page={}&tab=repositories'.format(i) for i in range(1,5))

    def parse(self, response):
        for repository in response.xpath('.//div[@id="user-repositories-list"]/ul[@    data-filterable-for="your-repos-filter"]/li'):
            yield ShiyanlougithubItem({
                'name': repository.xpath('.//a[@itemprop="name codeRepository"]/text()').re_first('[\w\-\_]+'),
                'update_time': repository.xpath('.//div[@class="f6 text-gray mt-2"]/relative-time/@datetime').extract_first(default='Missing')
            })
