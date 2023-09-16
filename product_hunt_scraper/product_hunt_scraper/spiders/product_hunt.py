import scrapy
from scrapy_redis.spiders import RedisSpider
from selenium import webdriver
from selenium.webdriver.chrome.options import Options as ChromeOptions

from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
from typing import Generator


class ProductHuntSpider(RedisSpider):
    name = 'product_hunt'
    redis_key = 'product_hunt:start_urls'

    custom_settings = {
        'DOWNLOAD_DELAY': 3,
        'USER_AGENT': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.36'
    }

    def parse(self, response: scrapy.http.Response) -> Generator[dict, None, None]:
        """Initialize the web driver and start requests by iterating over start URLs."""

        # Configure the Chrome WebDriver
        options = ChromeOptions()
        # Uncomment the next line if you want to run Chrome in headless mode
        # options.add_argument('--headless')
        driver = webdriver.Chrome(options=options)

        try:
            driver.get(response.url)
            last_height = driver.execute_script(
                "return document.body.scrollHeight")

            while True:
                driver.execute_script(
                    "window.scrollTo(0, document.body.scrollHeight);")
                try:
                    WebDriverWait(driver, 10).until(lambda d: d.execute_script(
                        "return document.body.scrollHeight") > last_height)
                except TimeoutException:
                    break

                new_height = driver.execute_script(
                    "return document.body.scrollHeight")
                if new_height == last_height:
                    break
                last_height = new_height

            page_source = driver.page_source
            response = scrapy.http.HtmlResponse(
                url=response.url, body=page_source, encoding='utf-8')

            self.logger.info(f"Processing: {response.url}")
            self.logger.info(f"Response status: {response.status}")
            self.logger.info(
                f"Number of links found: {len(response.css('a.styles_title__HzPeb'))}")

            for a_tag in response.css('a.styles_title__HzPeb'):
                text = a_tag.css('::text').get().strip()
                href = a_tag.css('::attr(href)').get().strip()
                self.logger.info(f"Extracted text: {text}")
                self.logger.info(f"Extracted href: {href}")
                yield {
                    'text': text,
                    'href': href
                }
        except Exception as e:
            self.logger.error(e)
        finally:
            driver.quit()
