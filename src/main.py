from deadstockfinder import deadstockfinder


def find_prices(name, size):
    finder = deadstockfinder()
    prices = []

    stockx = finder.find_stockx(name, size)
    for sneaker in stockx:
        if sneaker['price'] is not None:
            prices.append({
                'name': sneaker['name'],
                'price': sneaker['price'],
                'url': sneaker['url'],
                'img': sneaker['image'],
                'platform': 'StockX'
            })

    goat = finder.find_goat(name, size)
    for sneaker in goat:
        if sneaker['price'] is not None:
            prices.append({
                'name': sneaker['name'],
                'price': sneaker['price'],
                'url': sneaker['url'],
                'img': sneaker['image'],
                'platform': 'GOAT'
            })

    flightclub = finder.find_flightclub(name, size)
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
            result += f"\n{price_info['name']}, Size {size}: ${price_info['price']:.2f} on {price_info['platform']}.\nLink: {price_info['url']}\nImage: {price_info['img']}\n"
        return result
    else:
        return f"Unable to find the prices for {name}."


name = input("Enter the name of the sneaker: ")
size = input("Enter the size of the sneaker: ")
result = find_prices(name, size)
print(result)
print("\n")
print("Please note that the prices for some GOAT.com products may be a few dollars off the actual price.")
