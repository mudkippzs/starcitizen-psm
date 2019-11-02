from bs4 import BeautifulSoup as BS4
from io import BytesIO, StringIO
from termcolor import colored
from urllib3.exceptions import HTTPError

import certifi
import gzip
import io
import logging
import re
import urllib3

class Scanner:

	attrs = {}
	#Setup urllib3 PoolManager
	http = urllib3.PoolManager(cert_reqs='CERT_REQUIRED',ca_certs=certifi.where())
	ship_list = []
	watch_list = ['Caterpillar','Prospector']

	def set(self, attr, val):
		self.attrs[attr] = val
		return

	def check_url(self):
		responses = []
		if self.attrs["url"]:
			for url in self.attrs["url"]:
				responses.append(self.http.request('GET', url))
			return responses
		else:
			return False
	
	def create_http_request(self, url):
		return self.http.request('GET', url)

	def get_compressed_stream(self, data):
		return BytesIO(data)

	def create_soup_object(self, compressedData):
		return BS4(compressedData, "html.parser")

	def get_html(self):
		soups = []
		if self.check_url():
			for url in self.attrs["url"]:
				try:				
					response = self.create_http_request(url)
				except (HTTPError) as error:
					logging.exception("Data of %s not retrieved because %s\nURL: %s", error, url)
				except timeout:
					logging.exception("Socket timed out - URL %s", url)
					raise
				else:
					logging.info("Access successful.")
				try:
					compressedStream = self.get_compressed_stream(response.data)
					soup = self.create_soup_object(compressedStream)
					if soup and isinstance(soup, BS4):
						soups.append(soup)
					else:
						logging.error("No soup for you!")						
				except (IOError, AttributeError) as e:
					logging.exception(response)
					logging.exception("Exception raised: " + str(e))
					pass # Only triggers in tests and odd circumstances	

			return soups
		else:
			return False

	def get_ship_list(self):

		if self.check_url():
			pages = self.get_html()
			ship_names = self.extract_ships(pages)
			return ship_names
		else:
			return False

	def format_state(self, state):
		if 'Sold out' in state:
			return colored(state, 'red', attrs=['blink'])
		if 'In stock' in state:
			return colored(state, 'green', attrs=['bold'])

	def format_watched_ship(self, name):
		for ship in self.watch_list:
			if ship in self.watch_list:
				return colored(name, 'cyan', attrs=['blink','bold'])
		return name

	def extract_ships(self, pages):
		for html in pages:
			if isinstance(html, BS4):
				ship_blocks = html.find_all("div",{"class": "product-item"})			
				for ship in ship_blocks:
					try:					
						name = ship.find("div",{"class": "title"}).text.strip()
						price = ship.find("div",{"class": "price"}).text.strip()
						state = ship.find("span",{"class": "state"}).text.strip()
						formatted_state = self.format_state(state)
						self.ship_list.append({'name': name, 'price': price, 'state': state})
					except:
						raise

		return self.ship_list


	def print_ship_list(self):
		self.get_ship_list()

		for ship in self.ship_list:			
			print("%s\n\t%s\t%s" % (ship['name'], ship['price'], ship['state']))



