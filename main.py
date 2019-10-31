import scanner
import sys
import time

SC_Scanner = scanner.Scanner()	

def main():
	SC_Scanner.set("url", "https://robertsspaceindustries.com/pledge/extras?product_id=72")
	while True:
		now = time.ctime()
		print("\nShip Price Update (%s)" % (now))
		update()
		sys.stdout.flush()
		time.sleep(60)		
		print("\n\n\n")

def update():
	SC_Scanner.print_ship_list()


if __name__ == '__main__':
	main()