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

    def stockx(self, name, size):
        size = size.replace(".", "-")
        url = f"https://stockx.com/search/sneakers/size-{size}?size_types=men&s={name}"

        driver = self.driver_init()

        try:
            driver.get(url)
            driver.execute_script(
                "window.scrollTo(0, document.body.scrollHeight);")
            driver.implicitly_wait(1000)
            wait = WebDriverWait(driver, 100)
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
                    'image': image_element.split(',')[0][:-3].replace("w=140&h=75", "w=750")
                })

            return results
        except:
            return results

    def goat(self, name, size):
        url = f"https://www.goat.com/search?query={name}&size_converted=us_sneakers_men_{size}"

        driver = self.driver_init()

        try:
            driver.get(url)
            driver.execute_script(
                "window.scrollTo(0, document.body.scrollHeight);")
            driver.implicitly_wait(1000)
            wait = WebDriverWait(driver, 100)
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

    def flightclub(self, name, size):
        url = f"https://www.flightclub.com/catalogsearch/result?query={name}&size_men={size}"

        driver = self.driver_init()

        try:
            driver.get(url)
            driver.execute_script(
                "window.scrollTo(0, document.body.scrollHeight);")
            driver.implicitly_wait(1000)
            wait = WebDriverWait(driver, 100)
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

    def search(self, name, size):
        prices = []

        stockx = self.stockx(name, size)
        for sneaker in stockx:
            if sneaker['price'] is not None:
                prices.append({
                    'name': sneaker['name'],
                    'price': sneaker['price'],
                    'url': sneaker['url'],
                    'img': sneaker['image'],
                    'platform': 'StockX'
                })

        goat = self.goat(name, size)
        for sneaker in goat:
            if sneaker['price'] is not None:
                prices.append({
                    'name': sneaker['name'],
                    'price': sneaker['price'],
                    'url': sneaker['url'],
                    'img': sneaker['image'],
                    'platform': 'GOAT'
                })

        flightclub = self.flightclub(name, size)
        for sneaker in flightclub:
            if sneaker['price'] is not None:
                prices.append({
                    'name': sneaker['name'],
                    'price': sneaker['price'],
                    'url': sneaker['url'],
                    'img': sneaker['image'],
                    'platform': 'Flight Club'
                })

        sorted_prices = sorted(prices, key=lambda x: x['price'])

        if sorted_prices:
            result = ''
            for price_info in sorted_prices:
                result += f"\n{price_info['name']}, Size {size}: ${price_info['price']:.2f} on {price_info['platform']}."
                if "https://" in price_info['url']:
                    result += f"\nLink: {price_info['url']}"
                if "https://" in price_info['img']:
                    result += f"\nImage: {price_info['img']}"
                result += "\n"
            return result
        else:
            return f"Unable to find prices for: {name}."
