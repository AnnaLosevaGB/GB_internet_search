import scrapy
from castorama.items import CastoramaItem
from scrapy.loader import ItemLoader


class CastSpider(scrapy.Spider):
    name = "cast"
    allowed_domains = ["castorama.ru"]

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.start_urls = [f"https://www.castorama.ru/catalogsearch/result/?q={kwargs.get('search')}"]

    def parse(self, response):
        links = response.xpath("//a[@class='product-card__name ga-product-card-name']")
        for link in links:
            yield response.follow(link, callback=self.goods_parse)
        next_page = response.xpath("//a[@class='next i-next']/@href").get()
        if next_page:
            yield response.follow(next_page, callback=self.parse)

    def goods_parse(self, response):
        loader = ItemLoader(item=CastoramaItem(), response=response)
        loader.add_xpath('name', "//h1/text()")
        loader.add_xpath('price', "//span[@class='regular-price']/span/span/span/text()")
        loader.add_value('link', response.url)
        loader.add_xpath('photos', "//div[@class='js-zoom-container']//@data-src")
        loader.add_xpath('char_label',
                         "//div[@id='specifications']//dt[contains(@class, 'specs-table__attribute')]/span/text()")
        loader.add_xpath('char_value',
                         "//div[@id='specifications']//dd[contains(@class, 'specs-table__attribute')]//text()")

        yield loader.load_item()
