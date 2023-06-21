from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


class deadstockfinder:
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
        size = size.replace(".", "-")
        url = f"https://stockx.com/search/sneakers/size-{size}?size_types=men&s={name}"

        driver = self.driver_init()

        try:
            driver.get(url)
            driver.execute_script(
                "window.scrollTo(0, document.body.scrollHeight);")
            driver.implicitly_wait(1000)
            wait = WebDriverWait(driver, 10)
            results = []

            product_items = wait.until(EC.visibility_of_all_elements_located(
                (By.XPATH,
                 "//div[@class='css-111hzm2-GridProductTileContainer']")
            ))

            for item in product_items:
                name_element = item.find_element(
                    By.XPATH, ".//p[@class='chakra-text css-3lpefb']")
                price_element = item.find_element(
                    By.XPATH, ".//p[@class='chakra-text css-nsvdd9']")
                url_element = item.find_element(
                    By.XPATH, ".//a").get_attribute("href")
                image_element = item.find_element(
                    By.XPATH, ".//img").get_attribute("srcset")

                results.append({
                    'name': name_element.text.strip(),
                    'price': float(price_element.text.strip()[1:].replace(",", "")),
                    'url': url_element,
                    'image': image_element.split(',')[0][:-3]
                })

            return results
        except:
            return results

    def find_goat(self, name, size):
        url = f"https://www.goat.com/search?query={name}&size_converted=us_sneakers_men_{size}"

        driver = self.driver_init()

        try:
            driver.get(url)
            driver.execute_script(
                "window.scrollTo(0, document.body.scrollHeight);")
            driver.implicitly_wait(1000)
            wait = WebDriverWait(driver, 10)
            results = []

            product_items = wait.until(EC.visibility_of_all_elements_located(
                (By.XPATH, "//div[@data-qa='grid_cell_product']")
            ))

            for item in product_items:
                name_element = item.find_element(
                    By.XPATH, ".//div[@data-qa='grid_cell_product_name']")
                price_element = item.find_element(
                    By.XPATH, ".//div[@data-qa='grid_cell_product_price']")
                url_element = item.find_element(
                    By.XPATH, ".//a").get_attribute("href")
                image_element = item.find_element(
                    By.XPATH, ".//img").get_attribute("src")

                results.append({
                    'name': name_element.text.strip(),
                    'price': float(price_element.text.strip()[1:].replace(",", "")),
                    'url': url_element,
                    'image': image_element
                })

            return results
        except:
            return results

    def find_flightclub(self, name, size):
        url = f"https://www.flightclub.com/catalogsearch/result?query={name}&size_men={size}"

        driver = self.driver_init()

        try:
            driver.get(url)
            driver.execute_script(
                "window.scrollTo(0, document.body.scrollHeight);")
            driver.implicitly_wait(1000)
            wait = WebDriverWait(driver, 10)
            results = []

            product_items = wait.until(EC.visibility_of_all_elements_located(
                (By.XPATH, "//a[@data-qa='ProductItemsUrl']")
            ))

            for item in product_items:
                name_element = item.find_element(
                    By.XPATH, ".//h2[@data-qa='ProductItemTitle']")
                price_element = item.find_element(
                    By.XPATH, ".//div[@data-qa='ProductItemPrice']")
                url_element = item.get_attribute("href")
                image_element = item.find_element(
                    By.XPATH, ".//img").get_attribute("src")

                results.append({
                    'name': name_element.text.strip(),
                    'price': float(price_element.text.strip()[1:].replace(",", "")),
                    'url': url_element,
                    'image': image_element
                })

            return results
        except:
            return results
