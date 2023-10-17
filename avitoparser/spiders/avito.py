import scrapy
from scrapy_splash import SplashRequest
from avitoparser.items import AvitoparserItem
from scrapy.loader import ItemLoader


class AvitoSpider(scrapy.Spider):
    name = "avito"
    allowed_domains = ["avito.ru"]
    # start_urls = ["https://www.avito.ru/all?q=%D0%BA%D0%BE%D1%82%D1%8F%D1%82%D0%B0"]

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.start_urls = [f"https://www.avito.ru/all?q={kwargs.get('search')}"]

    def start_requests(self):
        if not self.start_urls and hasattr(self, "start_url"):
            raise AttributeError(
                "Crawling could not start: 'start_urls' not found "
                "or empty (but found 'start_url' attribute instead, "
                "did you miss an 's'?)"
            )
        for url in self.start_urls:
            yield SplashRequest(url)

    def parse(self, response):
        links = response.xpath("//a[@itemprop='url']/@href").getall()
        for link in links:
            yield SplashRequest("https://avito.ru" + link, callback=self.parse_ads)
        # next_page = response.xpath("//a[contains(@data-marker, 'nextPage')]/@href").get()
        # if next_page:
        #     yield response.follow(next_page, callback=self.parse)

    def parse_ads(self, response):
        print()
        loader = ItemLoader(item=AvitoparserItem(), response=response)
        loader.add_value('link', response.url)
        loader.add_xpath('name', "//h1/span[@itemprop='name']/text()")
        loader.add_xpath('price', "//meta[@itemprop='price']//text()")
        loader.add_xpath('description', "//div[@itemprop='description']//text()")
        loader.add_xpath('photos', "//img/@src")
        yield loader.load_item()
