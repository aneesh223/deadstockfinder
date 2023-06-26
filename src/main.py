from backend import deadstockfinder

finder = deadstockfinder()

name = input("Enter the name of the sneaker: ")
size = input("Enter the size of the sneaker: ")

result = finder.search(name, size)
print(result)
print("Please note that the prices for some Flight Club products may be a few dollars off the actual price, as their website isn't updated consistently.")
print("\n")