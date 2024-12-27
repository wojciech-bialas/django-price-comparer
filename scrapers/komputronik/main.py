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
        pages = self.driver.find_element("css selector", "li.flex:nth-child(8)").text
        pages = self.driver.find_element("css selector", "li.inline-flex > p:nth-child(2)").text
        return int(pages) if pages is not None else 1

    def next(self):
        try:
            btn = self.driver.find_element("css selector", "a.router-link-active.router-link-exact-active.flex.size-full.items-center.justify-center > i.i-arrow-right")
            btn.click()
        except NoSuchElementException as err:
            raise err
        except ElementClickInterceptedException:
            print('clicking next intercepted')

    def close_popup(self):
        try:
            btn = self.driver.find_element("xpath", '//*[@id="onetrust-accept-btn-handler"]')
            btn.click()
        except NoSuchElementException as err:
            raise err
    
    def close_question(self):
        try:
            btn = self.driver.find_element("xpath", "/html/body/div/div[2]/div/button[2]")
            btn.click()
        except NoSuchElementException as err:
            raise err
    

    def main(self):
        for cat, link in self.links.items():            
            self.driver.get(link)

            sleep(10)
            try:
                self.close_popup()
            except Exception:
                pass

            sleep(10)
            try:
                self.close_question()
            except Exception:
                pass

            # for _ in range(1, self.pages()):
            while True:
                names = self.driver.execute_script('''
                    return Array.from(document.querySelectorAll("h2.line-clamp-3")).map(x => x.innerText)
                    ''')
                    
                links = self.driver.execute_script('''
                    return Array.from(document.querySelectorAll("div.md\\\\:col-span-2 > a")).map(x => x.href)
                    ''')

                images = self.driver.execute_script('''
                    return Array.from(document.querySelectorAll('img.p-8')).map(x => x.src)
                    ''')

                pre_prices = self.driver.execute_script('''
                    return Array.from(document.querySelectorAll("div.my-2")).map(x => x.innerText)
                    ''')
                prices = [''.join(el[0:-2].split()) for el in pre_prices]

                pre_codes = self.driver.execute_script('''
                    return Array.from(document.querySelectorAll("div.mt-6.text-xs.text-gray-gravel > p:nth-of-type(2)")).map(x => x.innerText)
                    ''')
                codes = [x.split()[2] for x in pre_codes]

                self.send_to_api(names, links, images, prices, codes, cat)

                try:
                    self.next()
                except Exception:
                    break

                sleep(10)

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
