from sneakerfinder import SneakerFinder


def find_prices(name, size):
    finder = SneakerFinder()
    stockx = finder.find_stockx(name, size)
    goat = finder.find_goat(name, size)
    ebay = finder.find_ebay(name, size)
    prices = []

    for sneaker in stockx:
        if sneaker['price'] is not None:
            prices.append({
                'name': sneaker['name'],
                'price': sneaker['price'],
                'url': sneaker['url'],
                'platform': 'StockX'
            })

    for sneaker in goat:
        if sneaker['price'] is not None:
            prices.append({
                'name': sneaker['name'],
                'price': sneaker['price'],
                'url': sneaker['url'],
                'platform': 'GOAT'
            })

    for sneaker in ebay:
        if sneaker['price'] is not None:
            prices.append({
                'name': sneaker['name'],
                'price': sneaker['price'],
                'url': sneaker['url'],
                'platform': 'eBay'
            })

    sorted_prices = sorted(prices, key=lambda x: x['price'])

    if sorted_prices:
        result = ''
        for price_info in sorted_prices:
            result += f"\n{price_info['name']}, Size {size}: ${price_info['price']:.2f} on {price_info['platform']}. {price_info['url']}\n"
        return result
    else:
        return f"Unable to find the prices for {name}."


name = input("Enter the name of the sneaker (include Gender): ")
size = input("Enter the size of the sneaker: ")
result = find_prices(name, size)
print(result)
print("\n")
print("Please note that the prices for some GOAT.com products may be a few dollars off the actual price.\nThis program only collects mens sizes from GOAT.com for not.")
