import scanner
import unittest
from unittest.mock import patch


class ScannerTestcase(unittest.TestCase):

	def setUp(self):
		super(ScannerTestcase)
		self.testURL = "https://robertsspaceindustries.com/pledge/extras?product_id=72"		

	def test_scanner_import(self):
		self.assertTrue(scanner)

	def test_scanner_import_create_new_scanner(self):
		testScanner = scanner.Scanner()
		self.assertIsInstance(testScanner, type(scanner.Scanner()))

	def test_scanner_set_url(self):
		testScanner = scanner.Scanner()
		testScanner.set("url", self.testURL)
		self.assertEqual(testScanner.attrs['url'], self.testURL)

	@patch.object(scanner.Scanner.http, 'request', return_value=200, autospec=True)
	def test_scanner_ping_url(self, mockHTTPResp):
		testScanner = scanner.Scanner()
		testScanner.set("url", self.testURL)
		expected_response_code = 200
		self.assertEqual(testScanner.check_url(), expected_response_code)

	@patch.object(scanner.Scanner, 'get_compressed_stream', return_value="<html><body></body></html>")
	def test_scanner_get_html(self, mockCompressedStream):
		with patch.object(scanner.Scanner, 'create_http_request') as mockURLLIB3:
			testScanner = scanner.Scanner()
			testScanner.set("url", self.testURL)
			html = testScanner.get_html()			
			self.assertTrue(True if "<html" in str(html) else False)

	def test_scanner_list_ships(self):
		testScanner = scanner.Scanner()
		testScanner.set("url", self.testURL)
		list_of_ships = testScanner.get_ship_list()
		self.assertTrue(list_of_ships)


if __name__ == '__main__':
	unittest.main()