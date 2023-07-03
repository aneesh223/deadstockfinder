from .backend import deadstockfinder

finder = deadstockfinder()

name = input("Enter the name of the sneaker: ")
size = input("Enter the size of the sneaker: ")

result = finder.search(name, size)
print(result)