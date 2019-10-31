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

def main():
	SC_Scanner.set("url", "https://robertsspaceindustries.com/pledge/extras?product_id=72")
	while True:		
		update()
		sys.stdout.flush()
		time.sleep(86400)				

def update():
	now = time.ctime()
	print("\nShip Price Update (%s)" % (now))		
	SC_Scanner.print_ship_list()
	print("\n\n\n")


if __name__ == '__main__':
	motd()
	main()