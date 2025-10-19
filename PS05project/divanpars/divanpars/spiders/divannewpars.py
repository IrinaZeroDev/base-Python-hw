import scrapy


class DivannewparsSpider(scrapy.Spider):
    name = "divannewpars"
    allowed_domains = ["https://divan.ru"]
    start_urls = ["https://www.divan.ru/category/svet"]

    def parse(self, response):
        """Парсинг отрендеренной страницы"""
        self.logger.info(f'Response length: {len(response.text)} chars')

        # Ищем карточки товаров
        items = response.css('div.ProductCard_container__HLDPH')
#        cards = response.css('div.CatalogContent_list__PHgQQ')  # актуальный класс

        for item in items:
            yield {
                'name': item.css("div.ProductCard_info__c9Z_4 span::text").get(),
                'price': item.css("div.ProductCard_wrapperPrice__91mtE span.ui-LD-ZU::text").get(),
                'url': item.css("a::attr(href)").get()
            }
