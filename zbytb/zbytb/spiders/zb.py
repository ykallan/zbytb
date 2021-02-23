import scrapy
import re


class ZbSpider(scrapy.Spider):
    name = 'zb'
    allowed_domains = ['zbytb.com']
    start_urls = ['http://zbytb.com/']

    def start_requests(self):
        url_search = 'https://www.zbytb.com/search/'
        yield scrapy.Request(url=url_search, callback=self.parse)

    def parse(self, response):
        arts = response.xpath('//td[@class="zblist_xm"]/a/@href').getall()
        for one_art in arts:
            # print(one_art)
            yield response.follow(url=one_art, callback=self.parse_detail)

        next_pages = response.xpath('//div[@class="pages"]/a/@href').getall()
        if next_pages:
            for one_page in next_pages:
                yield response.follow(url=one_page, callback=self.parse)

    def parse_detail(self, response):

        lianxiren = re.findall(r'联系人：(\w+)<', response.text)
        if lianxiren:
            lianxiren = lianxiren[0]

        shouji = re.findall(r'br />手机：(\d{11})', response.text)
        if shouji:
            shouji = shouji[0]

        dianhua = re.findall(r'br />电话：(\d+-\d+)', response.text)
        if dianhua:
            dianhua = dianhua[0]

        youxiang = re.findall(r'br />邮箱：(.*?)<', response.text)
        if youxiang:
            youxiang = youxiang[0]

        # print(lianxiren, dianhua, shouji, youxiang)
        title = response.xpath('//p[@id="title"]/text()').get()
        release_time = response.xpath('//span[@class="color_9"]/text()').get()
        release_source = response.xpath('//p[@class=" t_c h_50"]/a/text()').getall()
        if release_source:
            release_source = release_source[:-1]

        # print(title, release_time, release_source)

        item = {}
        item['lianxiren'] = lianxiren
        item['dianhua'] = dianhua
        item['shouji'] = shouji
        item['youxiang'] = youxiang
        item['title'] = title
        item['release_time'] = release_time
        item['release_source'] = release_source
        yield item
