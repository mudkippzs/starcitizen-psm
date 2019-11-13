from PySide2.QtWidgets import (QApplication, QLabel, QPushButton,
                               QVBoxLayout, QWidget)
from sc_widget import StarCitizenShipPrices
import scanner
import sys
import time

SC_Scanner = scanner.Scanner()

def main():
	SC_Scanner.set("url", ["https://robertsspaceindustries.com/pledge/extras?product_id=72&sort=price_asc&search=&itemType=skus&storefront=pledge&type=extras&page=1",
		"https://robertsspaceindustries.com/pledge/extras?product_id=72&sort=price_asc&search=&itemType=skus&storefront=pledge&type=extras&page=2",
		"https://robertsspaceindustries.com/pledge/extras?product_id=72&sort=price_asc&search=&itemType=skus&storefront=pledge&type=extras&page=3"]
		)

	app = QApplication(sys.argv)
	widget = StarCitizenShipPrices(SC_Scanner)	
	sys.exit(app.exec_())

if __name__ == '__main__':		
	main()