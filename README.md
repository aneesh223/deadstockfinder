# deadstockfinder

deadstockfinder is a Python program that helps you find and compare prices of dead stock  sneakers across multiple online platforms. It utilizes web scraping with Selenium to retrieve data from popular sneaker marketplaces such as StockX, GOAT, and Flight Club. More sites will be added in the future.

## Requirements

- Python 3.x
- Selenium

## Installation

1. Clone the repository or download the source code files.
2. Install the required Python packages by running the following command:

   ```bash
   pip install selenium
3. Download the appropriate version of ChromeDriver that matches your Chrome browser version. You can find ChromeDriver downloads here: [ChromeDriver Downloads.](https://sites.google.com/chromium.org/driver/)

## Usage

1. Open a terminal or command prompt and navigate to the project directory.
2. Run the following command to start the program:

   ```bash
   python main.py
3. Enter the name of the sneaker when prompted. ex. Dunk Low Black Panda
4. Enter the size of the sneaker when prompted. ex. 10.5
5. The program will search for the given sneaker on StockX, GOAT, and Flight Club, and display the prices and links to the listings.

## Notes

- The program only collects prices for mens sizes for now. Womens sizes wil be added soon.
- The program retrieves the top listings from each platform and sorts them by price.

## Contributing
Contributions to the deadstockfinder project are welcome! If you find any issues or have suggestions for improvements, please open an issue or submit a pull request.

## License
This project is licensed under the MIT License.
