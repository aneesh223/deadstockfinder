from seleniumwire import webdriver as wdWithHeaders
from selenium import webdriver as wdNoHeaders
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


class deadstockfinder:
    def __init__(self):
        pass

    def interceptor(self, request):
        user_agent = "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Safari/537.36"
        sec_ch_ua = "\"Not.A/Brand\";v=\"8\", \"Chromium\";v=\"114\", \"Google Chrome\";v=\"114\""

        del request.headers["user-agent"]
        request.headers["user-agent"] = user_agent
        del request.headers["sec-ch-ua"]
        request.headers["sec-ch-ua"] = sec_ch_ua

    def driver_init(self, headers):
        options = Options()
        options.add_argument("--incognito")
        options.add_argument('--no-sandbox')
        options.add_argument('--disable-dev-shm-usage')
        options.add_argument("--headless=new")

        if isinstance(headers, bool):
            if headers:
                driver = wdWithHeaders.Chrome(options=options)
                driver.request_interceptor = self.interceptor
            else:
                driver = wdNoHeaders.Chrome(options=options)
            return driver

    def stockx(self, name, size):
        results = []

        try:
            size = size.replace(".", "-")
            url = f"https://stockx.com/search/sneakers/size-{size}?size_types=men&s={name}"

            driver = self.driver_init(True)
            driver.get(url)
            driver.execute_script(
                "window.scrollTo(0, document.body.scrollHeight);")
            driver.implicitly_wait(10)
            wait = WebDriverWait(driver, 10)

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
                
                try:
                    price_element = float(price_element.text.strip()[1:].replace(",", ""))
                except:
                    price_element = None

                results.append({
                    'name': name_element.text.strip(),
                    'price': price_element,
                    'url': url_element,
                    'image': image_element.split(',')[0][:-3].replace("w=140&h=75", "w=750")
                })

            print("StockX done")
        except Exception as e:
            print(f"StockX error: {str(e)}")

        return results

    def goat(self, name, size):
        results = []

        try:
            url = f"https://www.goat.com/search?query={name}&size_converted=us_sneakers_men_{size}"

            driver = self.driver_init(False)
            driver.get(url)
            driver.execute_script(
                "window.scrollTo(0, document.body.scrollHeight);")
            driver.implicitly_wait(10)
            wait = WebDriverWait(driver, 10)

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

                try:
                    price_element = float(price_element.text.strip()[1:].replace(",", ""))
                except:
                    price_element = None

                results.append({
                    'name': name_element.text.strip(),
                    'price': price_element,
                    'url': url_element,
                    'image': image_element
                })

            print("GOAT done")
        except Exception as e:
            print(f"GOAT error: {str(e)}")

        return results

    def flightclub(self, name, size):
        results = []

        try:
            url = f"https://www.flightclub.com/catalogsearch/result?query={name}&size_men={size}"

            driver = self.driver_init(True)
            driver.get(url)
            driver.execute_script(
                "window.scrollTo(0, document.body.scrollHeight);")
            driver.implicitly_wait(10)
            wait = WebDriverWait(driver, 10)

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
                
                try:
                    price_element = float(price_element.text.strip()[1:].replace(",", ""))
                except:
                    price_element = None

                results.append({
                    'name': name_element.text.strip(),
                    'price': price_element,
                    'url': url_element,
                    'image': image_element
                })

            print("Flight Club done")
        except Exception as e:
            print(f"Flight Club error: {str(e)}")

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
            result += "\nPlease note that the prices for some Flight Club products may be a few dollars off the actual price, as their website isn't updated consistently.\n"
            return result   
        else:
            return f"\nUnable to find prices for: {name}.\n"
