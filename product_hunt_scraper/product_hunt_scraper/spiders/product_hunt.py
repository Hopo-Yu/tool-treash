import scrapy
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from typing import Generator
from selenium.common.exceptions import TimeoutException


class ProductHuntSpider(scrapy.Spider):
    name = 'product_hunt'
    start_urls = ['http://www.producthunt.com/time-travel/2023/9']
    
    custom_settings = {
        'DOWNLOAD_DELAY': 3,
        'USER_AGENT': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.36'
    }

    def start_requests(self) -> Generator[scrapy.Request, None, None]:
        """Initialize the web driver and start requests by iterating over start URLs."""
        driver = webdriver.Chrome()

        try:
            for url in self.start_urls:
                driver.get(url)
                last_height = driver.execute_script("return document.body.scrollHeight")

                while True:
                    driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
                    try:
                        WebDriverWait(driver, 10).until(lambda d: d.execute_script("return document.body.scrollHeight") > last_height)
                    except TimeoutException:
                        break
                    
                    new_height = driver.execute_script("return document.body.scrollHeight")
                    if new_height == last_height:
                        break
                    last_height = new_height

                page_source = driver.page_source
                response = scrapy.http.HtmlResponse(url=url, body=page_source, encoding='utf-8')
                yield scrapy.Request(url, callback=self.parse, dont_filter=True, meta={'response': response})
        except Exception as e:
            self.logger.error(e)
        finally:
            driver.quit()


    def parse(self, response: scrapy.http.Response) -> Generator[dict, None, None]:
        """Parse the response to extract the desired data."""
        response = response.meta['response']
        for a_tag in response.css('a.styles_title__HzPeb'):
            text = a_tag.css('::text').get().strip()
            href = a_tag.css('::attr(href)').get().strip()
            yield {
                'text': text,
                'href': href
            }
