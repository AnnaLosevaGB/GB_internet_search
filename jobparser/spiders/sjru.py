import scrapy
from scrapy.http import HtmlResponse
from jobparser.items import JobparserItem


class SjruSpider(scrapy.Spider):
    name = "sjru"
    allowed_domains = ["superjob.ru"]
    start_urls = ["https://www.superjob.ru/vakansii/sadovnik.html"]

    def parse(self, response: HtmlResponse, **kwargs):
        links = response.xpath("//div[@class='f-test-search-result-item']//a[contains(@href, '/vakansii')]/@href").getall()
        for link in links:
            yield response.follow(link, callback=self.vacancy_parse)
        next_page = response.xpath("//a[@class='f-test-button-dalshe']/@href").get()
        if next_page:
            yield response.follow(next_page, callback=self.parse)

    def vacancy_parse(self, response: HtmlResponse):
        name = response.xpath("//h1/text()").get()
        url = response.url
        salary = response.xpath("//h1/following-sibling::span/descendant::*/text()").getall()
        yield JobparserItem(name=name, salary=salary, url=url)
        print(name, url, salary)
