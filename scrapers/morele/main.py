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
        self.pages = [
            'https://www.morele.net/kategoria/karty-graficzne-12/,,,,,,,,0,,,,,sprzedawca:m/'
        ]
        self.main()

    def close_popups(self):
        sleep(7)
        close_chat_button = self.driver.find_element("xpath", "/html/body/div[10]/div/div/div[2]/div[1]/button/i")
        close_chat_button.click()
        sleep(2)
        close_gdpr_info = self.driver.find_element("xpath", "/html/body/div[2]/div/div/button")
        close_gdpr_info.click()
        sleep(2)

    def navigate_to(self):
        menu = self.driver.find_element("xpath",
                                        "/html/body/header/div[2]/div/div/div/nav[1]/div[2]/div[2]/div/ul/li[1]/a/span")
        submenu = self.driver.find_element("xpath",
                                           "/html/body/header/div[2]/div/div/div/nav[1]/div[2]/div[2]/div/ul/li[1]/div/div[3]/ul[1]/li[1]/ul/li[1]/a")
        action = ActionChains(self.driver)
        action.move_to_element(menu)
        action.perform()
        sleep(1)
        submenu.click()

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

    def scrape_products_from_page(self):
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

        ProductSerializer(names, links, images, prices, "morele")

    def click_next(self):
        try:
            next_page = self.driver.find_element("css selector", "ul.pagination.dynamic > li:last-child")
            next_page.click()
        except NoSuchElementException as err:
            raise err

    def scrape_laptops(self):
            for _ in range(1, self.number_of_pages()):
                sleep(2)
                self.scrape_products_from_page()
                self.click_next()

    # returns a list of tuples
    def make_list_of_tuples(self, a, b, c, d, e):
        return list(zip(a, b, c, d, e))

    def add_to_db(self, iter):
        self.cur.executemany(f'''INSERT INTO morele
                             (name, link, image, price, date)
                             VALUES (%s,%s,%s,%s,%s);''', iter)
        self.conn.commit()

    def main(self):
        self.driver.get(self.pages[0])
        sleep(5)
        self.close_cookie_box()
        self.scrape_laptops()
        self.driver.quit()


class ProductSerializer:

    def __init__(self, names, links, images, prices, shop) -> None:
        self.names = self.create_names(names)
        self.links = links
        self.images = images
        self.prices = prices
        self.codes = self.create_codes(names)
        self.shop = shop
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
