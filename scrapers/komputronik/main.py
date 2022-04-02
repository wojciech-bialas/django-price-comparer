import requests
from requests.exceptions import RequestException
from selenium import webdriver
from selenium.webdriver.common.action_chains import ActionChains
from selenium.common.exceptions import NoSuchElementException, ElementClickInterceptedException, StaleElementReferenceException
from time import sleep
from datetime import date
from urllib3 import Timeout
import re
import json


class KomputronikScrapper:

    def __init__(self):
        self.options = webdriver.FirefoxOptions()
        self.driver = webdriver.Firefox()
        self.driver.implicitly_wait(10)
        self.action = ActionChains(self.driver)
        self.page = 'https://www.komputronik.pl/category/1099/karty-graficzne.html?alt=1&showBuyActiveOnly=1'
        self.shop = 'komputronik'
        self.date = date.today().strftime("%Y-%m-%d")
        self.headers = {'Accept' : 'application/json', 'Content-Type' : 'application/json'}
        self.main()

    def pages(self):
        pages = self.driver.find_element("xpath", "/html/body/ktr-site/div/div[2]/ktr-product-list/div/ktr-transclude/div[1]/div[4]/div[5]/div/ul/li[5]/a").text
        return int(pages) if pages is not None else 1

    def next(self):
        try:
            btn = self.driver.find_element("css selector", "div.pagination.text-xs-center.text-lg-right.isp-top-10 > ul > li:last-child > a")
            btn.click()
        except NoSuchElementException as err:
            raise err
        except ElementClickInterceptedException:
            pass

    def close_popup(self):
        try:
            btn = self.driver.find_element("xpath", "/html/body/ktr-site/ktr-cookie-law/div/div/div/div/div[2]/a")
            btn.click()
        except NoSuchElementException as err:
            raise err        

    def main(self):
        self.driver.get(self.page)
        sleep(5)
        self.close_popup()
        sleep(1)

        for _ in range(1, self.pages()):
            names = self.driver.execute_script('''
                return Array.from(document.querySelectorAll("a.blank-link")).map(x => x.innerText)
                ''')
                
            links = self.driver.execute_script('''
                return Array.from(document.querySelectorAll("a.blank-link")).map(x => x.href)
                ''')

            images = self.driver.execute_script('''
                return Array.from(document.querySelectorAll('a.pe2-img > img')).map(x => x.src)
                ''')

            pre_prices = self.driver.execute_script('''
                return Array.from(document.querySelectorAll("span.proper")).map(x => x.innerText)
                ''')

            prices = [''.join(el[0:-2].split()) for el in pre_prices]

            pre_codes = self.driver.execute_script('''
                return Array.from(document.querySelectorAll("div.pe2-codes")).map(x => x.innerText)
                ''')
                
            codes = []
            ex = re.compile(r"\[(.*)\] K")
            for el in pre_codes:
                code = ex.findall(el)
                codes.extend(code)

            self.send_to_api(names, links, images, prices, codes)
            self.next()
            sleep(10)

        self.driver.quit()

    def send_to_api(self, names, links, images, prices, codes):
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
    KomputronikScrapper()
