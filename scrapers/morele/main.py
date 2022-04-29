import requests
from requests.exceptions import RequestException
from selenium import webdriver
from selenium.webdriver.common.action_chains import ActionChains
from selenium.common.exceptions import NoSuchElementException
from selenium.common.exceptions import StaleElementReferenceException
from time import sleep
from datetime import date
from urllib3 import Timeout
import re
import json


class MoreleScrapper:

    def __init__(self):
        self.options = webdriver.FirefoxOptions()
        self.driver = webdriver.Firefox()
        self.driver.implicitly_wait(10)
        self.action = ActionChains(self.driver)
        self.pages = {
            'gpu': 'https://www.morele.net/kategoria/karty-graficzne-12/,,,,,,,,0,,,,,sprzedawca:m/',
            'ram': 'https://www.morele.net/kategoria/pamieci-ram-38/,,,,,,,,0,,,,21239O668024,sprzedawca:m/1/?noi',
            'cpu': 'https://www.morele.net/kategoria/procesory-45/,,,,,,,,0,,,,,sprzedawca:m/1/'
        }
        self.main()

    def close_cookie_box(self):
        try:
            button = self.driver.find_element("xpath", "/html/body/div[5]/div/div/button")
            button.click()
        except NoSuchElementException:
            return

    def number_of_pages(self):
        pages = self.driver.execute_script('''
            return document.querySelector('ul.pagination').dataset.count
        ''')
        return int(pages) if pages is not None else 1

    def scrape_products_from_page(self, cat):
        names = self.driver.execute_script("""
            let table = [];
            let nodes = document.querySelectorAll('div[data-product-name]');
            nodes.forEach( (curVal) => {
                table.push(curVal.dataset.productName);
            });
            return table;
            """)

        links = self.driver.execute_script("""
            let table = [];
            let nodes = document.querySelectorAll('a[class=productLink]');
            nodes.forEach( (curVal) => {
                table.push(curVal.href);
            });
            return table;
            """)

        images = self.driver.execute_script("""
            let table = [];
            let nodes = document.querySelectorAll('img.product-image');
            nodes.forEach( (curVal) => {
                if (curVal.src) {
                    table.push(curVal.src);
                } else {
                    table.push(curVal.dataset.src);
                }
            });
            return table;
            """)

        prices = self.driver.execute_script("""
            let table = [];
            let nodes = document.querySelectorAll('div[data-product-price]');
            nodes.forEach( (curVal) => {
                table.push(curVal.dataset.productPrice);
            });
            return table;
            """)

        ProductSerializer(names, links, images, prices, "morele", cat)

    def click_next(self):
        try:
            next_page = self.driver.find_element("css selector", "ul.pagination.dynamic > li:last-child")
            next_page.click()
        except NoSuchElementException as err:
            raise err

    def main(self):
        for cat, link in self.pages.items():
            self.driver.get(link)
            sleep(5)
            try:
                self.close_cookie_box()
            except Exception:
                pass
            for _ in range(1, self.number_of_pages()):
                sleep(2)
                self.scrape_products_from_page(cat)
                self.click_next()
        self.driver.quit()


class ProductSerializer:

    def __init__(self, names, links, images, prices, shop, category) -> None:
        self.names = self.create_names(names)
        self.links = links
        self.images = images
        self.prices = prices
        self.codes = self.create_codes(names)
        self.shop = shop
        self.category = category
        self.date = date.today().strftime("%Y-%m-%d")
        self.headers = {'Accept' : 'application/json', 'Content-Type' : 'application/json'}
        self.send_products(self.names, self.codes, links, images, prices)

    def create_codes(self, names):
        codes = []
        ex = re.compile(r"\((.*)\)")
        for name in names:
            result = ex.findall(name)
            codes.extend(result)
        return codes

    def create_names(self, names):
        new = []
        for name in names:
            result = re.split(r"\((.*)\)", name)
            new.append(result[0].rstrip())
        return new

    def send_products(self, names, codes, links, images, prices):
        val = []
        for (name, code, link, image, price) in zip(names, codes, links, images, prices):
            product_dict = {
                "code": code,
                "name": name,
                "category": self.category,
                "link": link,
                "image": image,
                "shop": self.shop,
                "price": price,
                "date": self.date
            }
            val.append(product_dict)
        data = json.dumps(val)
        try:
            r = requests.post("http://127.0.0.1:8000/product/add", data=data, headers=self.headers)
            print(r.content)
        except RequestException as err:
            print(err.args)


if __name__ == '__main__':
    MoreleScrapper()
