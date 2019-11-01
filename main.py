import scanner
import sys
import time

SC_Scanner = scanner.Scanner()

def motd():
	print("""
===============================================
STAR CITIZEN - PLEDGE STORE MONITOR (PSM) v1.0a
===============================================
				(@uthor: github.com/mudkippzs)

usage: python main.py
Future updates will have cli options for alerts, timer setting etc.
		""")
	sys.stdout.flush()

def main():
	SC_Scanner.set("url", ["https://robertsspaceindustries.com/pledge/extras?product_id=72&sort=price_asc&search=&itemType=skus&storefront=pledge&type=extras&page=1",
		"https://robertsspaceindustries.com/pledge/extras?product_id=72&sort=price_asc&search=&itemType=skus&storefront=pledge&type=extras&page=2",
		"https://robertsspaceindustries.com/pledge/extras?product_id=72&sort=price_asc&search=&itemType=skus&storefront=pledge&type=extras&page=3"]
		)
	
	while True:		
		update()
		time.sleep(3600)				

def update():
	now = time.ctime()
	print("\nShip Price Update (%s)\n\n" % (now))	
	sys.stdout.flush()
	SC_Scanner.print_ship_list()
	sys.stdout.flush()
	print("\n\n\n")


if __name__ == '__main__':
	motd()
	sys.stdout.flush()
	main()