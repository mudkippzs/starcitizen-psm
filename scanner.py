from io import BytesIO, StringIO
from bs4 import BeautifulSoup as BS4
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

	def set(self, attr, val):
		self.attrs[attr] = val
		return

	def check_url(self):
		if self.attrs["url"]:
			response = self.http.request('GET', self.attrs["url"])
			return response
		else:
			print("Error: No URL set.")
			exit()
	
	def create_http_request(self):
		return self.http.request('GET', self.attrs["url"])

	def get_compressed_stream(self, data):
		return BytesIO(data)

	def create_soup_object(self, compressedData):
		return BS4(compressedData, "html.parser")

	def get_html(self):
		if self.check_url():
			raw_html = None
			try:				
				response = self.create_http_request()
			except (HTTPError) as error:
				logging.exception("Data of %s not retrieved because %s\nURL: %s", error, url)
			except timeout:
				logging.exception("Socket timed out - URL %s", url)
				raise
			else:
				logging.info("Access successful.")
			# End headers.
			# Send our request.
			# Uncompress the response and if its nonsense it will throw an exception, we don"t care about anything but a successful response
			try:
				compressedStream = self.get_compressed_stream(response.data)
				#gzipper = gzip.GzipFile(fileobj=compressedStream)
				#uncompressedStream = gzipper.read()
				soup = self.create_soup_object(compressedStream)
				if soup and isinstance(soup, BS4):
					return soup
				else:
					logging.error("No soup for you!")
					return False
			except (IOError, AttributeError) as e:
				logging.exception(response)
				logging.exception("Exception raised: " + str(e))
				pass # Only triggers in tests and odd circumstances	

			return raw_html
		else:
			return False

	def get_ship_list(self):

		if self.check_url():
			html = self.get_html()
			ship_names = self.extract_ships(html)
			return ship_names
		else:
			return False

	def extract_ships(self, html):
		if isinstance(html, BS4):
			ship_blocks = html.find_all("div",{"class": "product-item"})			
			for ship in ship_blocks:
				try:					
					name = ship.find("div",{"class": "title"}).text.strip()
					price = ship.find("div",{"class": "price"}).text.strip()
					state = ship.find("span",{"class": "state"}).text.strip()					
					self.ship_list.append({'name': name, 'price': price, 'state': state})
				except:
					raise

		return self.ship_list


	def print_ship_list(self):
		self.get_ship_list()

		for ship in self.ship_list:			
			print("%s\n\t%s\t%s" % (ship['name'], ship['price'], ship['state']))



