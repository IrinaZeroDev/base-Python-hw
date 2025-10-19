from scrapy import signals
from scrapy.http import HtmlResponse
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time


class SeleniumMiddleware:
    """Middleware для рендеринга JavaScript через Selenium"""

    def __init__(self):
        chrome_options = Options()
        chrome_options.add_argument('--headless')  # Без GUI
        chrome_options.add_argument('--no-sandbox')
        chrome_options.add_argument('--disable-dev-shm-usage')
        chrome_options.add_argument('--disable-gpu')
        chrome_options.add_argument('--disable-blink-features=AutomationControlled')
        chrome_options.add_argument('user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36')

        self.driver = webdriver.Chrome(options=chrome_options)

    def process_request(self, request, spider):
        """Обрабатываем запрос через Selenium"""
        self.driver.get(request.url)

        # Ждем загрузки контента (настройте под сайт)
        try:
            WebDriverWait(self.driver, 10).until(
                EC.presence_of_element_located((By.CLASS_NAME, "LlPhw"))
            )
            time.sleep(2)  # Дополнительная пауза для JS
        except:
            time.sleep(5)  # Если элемент не найден, ждем просто 5 сек

        # Получаем отрендеренный HTML
        body = self.driver.page_source

        # Возвращаем HtmlResponse с отрендеренным контентом
        return HtmlResponse(
            url=self.driver.current_url,
            body=body,
            encoding='utf-8',
            request=request
        )

    def spider_closed(self):
        """Закрываем браузер при завершении spider"""
        self.driver.quit()

    @classmethod
    def from_crawler(cls, crawler):
        middleware = cls()
        crawler.signals.connect(middleware.spider_closed, signal=signals.spider_closed)
        return middleware
