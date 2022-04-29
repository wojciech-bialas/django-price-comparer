import requests
from requests.exceptions import RequestException
from selenium import webdriver
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.keys import Keys
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
        self.links = {
            'gpu': 'https://www.komputronik.pl/category/1099/karty-graficzne.html?alt=1&showBuyActiveOnly=1',
            'ram': 'https://www.komputronik.pl/category/437/pamiec-ram.html?a%5B112422%5D%5B%5D=88133&filter=1&showBuyActiveOnly=1',
            'cpu': 'https://www.komputronik.pl/category/401/procesory.html?showBuyActiveOnly=1'
        }
        self.shop = 'komputronik'
        self.category = 'gpu'
        self.date = date.today().strftime("%Y-%m-%d")
        self.headers = {'Accept' : 'application/json', 'Content-Type' : 'application/json'}
        self.main()

    def pages(self):
        pages = self.driver.find_element("css selector", ".text-lg-right > ul:nth-child(1) > li:nth-child(5) > a:nth-child(1)").text
        return int(pages) if pages is not None else 1

    def next(self):
        try:
            btn = self.driver.find_element("css selector", "div.pagination.text-xs-center.text-lg-right.isp-top-10 > ul > li:last-child > a")
            btn.click()
        except NoSuchElementException as err:
            raise err
        except ElementClickInterceptedException:
            print('clicking next intercepted')

    def close_popup(self):
        try:
            btn = self.driver.find_element("xpath", "/html/body/ktr-site/ktr-cookie-law/div/div/div/div/div[2]/a")
            btn.click()
        except NoSuchElementException as err:
            raise err        

    def main(self):
        self.driver.get(self.links['gpu'])
        sleep(5)
        try:
            self.close_popup()
        except Exception:
            pass

        for cat, page in self.links.items():            
            sleep(2)
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

                self.send_to_api(names, links, images, prices, codes, cat)
                self.next()
                sleep(10)

            self.action.send_keys(Keys.HOME)
            self.action.perform()
            sleep(1)

            first_button = self.driver.find_element('css selector', '.at-cat-ELEKTRONIKA > a:nth-child(1) > span:nth-child(2)')
            hover = self.action.move_to_element(first_button)
            hover.perform()
            sleep(1)

            second_button = self.driver.find_element('css selector', 'li.at-cat-KOMPONENTY30 :first-child span')
            hover = self.action.move_to_element(second_button)
            hover.perform()
            sleep(1)
            if cat == 'gpu':
                third_button = self.driver.find_element('css selector', 'li.at-cat-KAMINTER :first-child span')
                hover = self.action.move_to_element(third_button)
                hover.perform()
                sleep(1)
                third_button.click()
                sleep(1)
                self.action.send_keys(Keys.ARROW_DOWN)
                self.action.send_keys(Keys.ARROW_DOWN)
                self.action.perform()
            elif cat == 'ram':
                third_button = self.driver.find_element('css selector', 'ul.dropdown-menulist:nth-child(2) > li:nth-child(2) > a:nth-child(1) > span:nth-child(1)')
                hover = self.action.move_to_element(third_button)
                hover.perform()
                sleep(1)
                third_button.click()
                sleep(1)
                self.action.send_keys(Keys.ARROW_DOWN)
                self.action.send_keys(Keys.ARROW_DOWN)
                self.action.perform()

        self.driver.quit()

    def send_to_api(self, names, links, images, prices, codes, category):
        val = []
        for (name, code, link, image, price) in zip(names, codes, links, images, prices):
            product_dict = {
                "code": code,
                "name": name,
                "category": category,
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
