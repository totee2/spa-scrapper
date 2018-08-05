# -*- coding: utf-8 -*-
import scrapy
from scrapy import Request

from spa.items import SpaItem


class SpeciesSpider(scrapy.Spider):
    name = 'crawlSpecies'
    allowed_domains = ['la-spa.fr']

    def __init__(self, url='', **kwargs):
        self.start_urls = [url]
        super(SpeciesSpider, self).__init__(**kwargs)

    def parse(self, response):
        results = response.xpath('//div[@class="block-result-search "]')

        for result in results:
            url = result.xpath('.//span[@class="refuge-name"]/a/@href').extract()
            if len(url) > 1:
                url = url[1]
            else:
                continue
            img = result.xpath('.//img/@src').extract_first()
            short_name = result.xpath('.//div[@class="field-item even"]/text()').extract_first()
            refuge_name = result.xpath('.//span[@class="refuge-name"]/a/text()').extract_first()
            animal = {'URL': url, 'img': img, 'short_name': short_name, 'refuge_name': refuge_name}
            details = Request(url, callback=self.parse_animal, meta=animal)

            yield details

        relative_next_url = response.xpath('//li[@class="pager-next"]/a/@href').extract_first()
        if relative_next_url is not None:
            absolute_next_url = "https://www.la-spa.fr" + relative_next_url
            yield Request(absolute_next_url, callback=self.parse)

    def parse_animal(self, response):
        name = response.xpath('//div[@class="field field-name-field-esp-ce field-type-list-text field-label-inline clearfix"]/div[@class="field-items"]/text()').extract_first()
        breed = response.xpath('//div[@class="field field-name-field-race field-type-text field-label-inline clearfix"]/div[@class="field-items"]/div/text()').extract_first()
        size = response.xpath('//div[@class="field field-name-field-taille field-type-list-text field-label-inline clearfix"]/div[@class="field-items"]/div/text()').extract_first()
        gender = response.xpath('//div[@class="field field-name-field-sexe field-type-list-boolean field-label-inline clearfix"]/div[@class="field-items"]/div/text()').extract_first()
        birthday = response.xpath('//div[@class="field field-name-field-date-naissance field-type-text field-label-inline clearfix"]/div[@class="field-items"]/div/text()').extract_first()
        description = response.xpath('//div[@class="field field-name-body field-type-text-with-summary field-label-hidden"]/div/div/p/text()').extract_first()

        image_array = response.xpath('//div[@class="content col-xs-12 col-sm-8 left-bar cat"]//img[contains(@src, "itok")]/@src').extract()

        url = response.meta.get('URL')
        img = response.meta.get('img')
        short_name = response.meta.get('short_name')
        refuge_name = response.meta.get('refuge_name')
        yield SpaItem(url=url, profile_picture=img, short_name=short_name, refuge_name=refuge_name,
                      name=name, breed=breed, size=size, gender=gender, birthday=birthday, description=description, image_urls=image_array)
