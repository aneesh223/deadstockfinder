from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
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
        url = f"https://stockx.com/search/sneakers/size-{size}?size_types=men&s={name}"

        driver = self.driver_init()

        try:
            driver.get(url)
            driver.implicitly_wait(10)
            wait = WebDriverWait(driver, 10)
            results = []

            for i in range(10):
                name = driver.find_elements(
                    By.XPATH, "//div[@class='css-111hzm2-GridProductTileContainer']//p[@class='chakra-text css-3lpefb']")[i]
                price = driver.find_elements(
                    By.XPATH, "//div[@class='css-111hzm2-GridProductTileContainer']//p[@class='chakra-text css-nsvdd9']")[i]
                url = driver.find_elements(
                    By.XPATH, "//div[@class='css-111hzm2-GridProductTileContainer']//a")[i]

                results.append({
                    'name': name.text.strip(),
                    'price': float(price.text.strip()[1:].replace(",", "")),
                    'url': url.get_attribute('href')
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
            wait = WebDriverWait(driver, 10)
            results = []

            for i in range(10):
                name = wait.until(EC.visibility_of_element_located((
                    By.XPATH, f"//div[@data-qa='grid_cell_product' and @data-grid-cell-position='{i+1}']//div[@data-qa='grid_cell_product_name']")))
                price = wait.until(EC.visibility_of_element_located((
                    By.XPATH, f"//div[@data-qa='grid_cell_product' and @data-grid-cell-position='{i+1}']//div[@data-qa='grid_cell_product_price']")))
                url = wait.until(EC.visibility_of_element_located((
                    By.XPATH, f"//div[@data-qa='grid_cell_product' and @data-grid-cell-position='{i+1}']//a")))

                results.append({
                    'name': name.text.strip(),
                    'price': float(price.text.strip()[1:].replace(",", "")),
                    'url': url.get_attribute('href')
                })

            return results
        except:
            return results

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
