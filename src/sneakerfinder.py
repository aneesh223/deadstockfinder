from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
import os
import requests
import json


class SneakerFinder:
    def __init__(self):
        pass

    def driver_init(self):
        options = Options()
        options.add_argument("--incognito")
        options.add_argument('--no-sandbox')
        options.add_argument('--disable-dev-shm-usage')
        # options.add_argument("--headless")

        driver = webdriver.Chrome(options=options)
        return driver

    def find_stockx(self, name, size):
        url = f'https://stockx.com/api/browse?_search={name}'

        headers = {
            'accept': 'application/json',
            'accept-encoding': 'utf-8',
            'accept-language': 'en-US,en;q-0.9',
            'referer': 'https://stockx.com',
            'sec-ch-ua': '"Not.A/Brand";v="8", "Chromium";v="114", "Google Chrome";v="114"',
            'sec-ch-ua-mobile': '?0',
            'sec-ch-ua-platform': '"macOS"',
            'sec-fetch-dest': 'empty',
            'sec-fetch-mode': 'cors',
            'sec-fetch-site': 'same-origin',
            'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Safari/537.36',
            'x-requested-with': 'XMLHttpRequest'
        }

        html = requests.get(url=url, headers=headers)
        output = json.loads(html.text)
        results = []
        try:
            for product in output['Products'][:5]:
                name = product['title']
                urlKey = product['urlKey']
                url = f"https://stockx.com/buy/{urlKey}?size={size}"

                driver = self.driver_init()
                driver.get(url)
                driver.implicitly_wait(10)

                price = driver.find_element(
                    By.XPATH, "//p[contains(@class, 'css-1b8s8v')]")

                results.append({
                    'name': name,
                    'price': float(price.text.strip()[1:].replace(",", "")),
                    'url': url
                })

            return results
        except:
            return results

    def find_goat(self, name, size):
        url = f"https://www.goat.com/search?query={name}&size_converted=us_sneakers_men_{size}"

        driver = self.driver_init()

        try:
            driver.get(url)
            driver.implicitly_wait(10)
            results = []

            for i in range(5):
                name = driver.find_element(
                    By.XPATH, f"//div[@data-qa='grid_cell_product' and @data-grid-cell-position='{i+1}']//div[@data-qa='grid_cell_product_name']")
                price = driver.find_element(
                    By.XPATH, f"//div[@data-qa='grid_cell_product' and @data-grid-cell-position='{i+1}']//div[@data-qa='grid_cell_product_price']")
                url = driver.find_element(
                    By.XPATH, f"//div[@data-qa='grid_cell_product' and @data-grid-cell-position='{i+1}']//a")

                results.append({
                    'name': name.text.strip(),
                    'price': float(price.text.strip()[1:].replace(",", "")),
                    'url': url.get_attribute('href')
                })

            return results

        except:
            return []

    def find_ebay(self, name, size):
        url = f"https://www.ebay.com/sch/i.html?_nkw={name}%20size%20{size}"

        driver = self.driver_init()

        driver.get(url)
        urls = []

        for i in range(5):
            element = driver.find_element(
                By.XPATH, f"//li[contains(@data-gr2, '{i+1}')]/div/div/a[@data-interactions]")
            urls.append(element.get_attribute("href"))

        results = []

        try:
            for url in urls:
                driver.get(url)

                name = driver.find_element(
                    By.XPATH, f"//h1[contains(@class, 'x-item-title__mainTitle')]/span[@class]")
                price = driver.find_element(
                    By.XPATH, f"//span[contains(@itemprop, 'price')]/span[@class]")
                results.append({
                    'name': name.text.strip(),
                    'price': float(price.text.strip()[4:].replace(",", "")),
                    'url': url
                })

            return results
        except:
            return results
