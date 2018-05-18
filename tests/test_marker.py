# -*- coding: utf-8 -*-
import unittest
import sys
sys.path.append('..')
from marker import marker

TEST_URL = 'http://localhost:8080/'

class TestGetMarkup(unittest.TestCase):

	def request_markup(self, tokens):
		markup_request = {
			'tokens': tokens,
			'inputs': { 'target_url': TEST_URL, 'min_n': 2}
		}
		return marker.get_markup(markup_request)

	def test_markup_contains_correct_groups_case_1(self):
		tokens = "Lorem ipsum dolor sit amet".split()
		resp = self.request_markup(tokens)
		self.assertTrue(resp['markup'][0]['group']['first'] == 0)
		self.assertTrue(resp['markup'][0]['group']['last'] == 4)


	def test_markup_contains_correct_groups_case_2(self):
		tokens = "consectetur adipisicing elit".split()
		resp = self.request_markup(tokens)
		self.assertTrue(resp['markup'][0]['group']['first'] == 0)
		self.assertTrue(resp['markup'][0]['group']['last'] == 2)

	def test_markup_contains_correct_groups_case_3(self):
		tokens = "consectetur adipisicing elit foo foo minim veniam".split()
		resp = self.request_markup(tokens)
		self.assertTrue(resp['markup'][0]['group']['first'] == 0)
		self.assertTrue(resp['markup'][0]['group']['last'] == 2)
		self.assertTrue(resp['markup'][1]['group']['first'] == 5)
		self.assertTrue(resp['markup'][1]['group']['last'] == 6)

	def test_markup_contains_correct_groups_case_4(self):
		tokens = "consectetur".split()
		resp = self.request_markup(tokens)
		self.assertTrue(len(resp['markup']) == 0)

	def test_markup_contains_correct_groups_case_5(self):
		tokens = "baz ipsum dolor foo bar".split()
		resp = self.request_markup(tokens)
		self.assertTrue(resp['markup'][0]['group']['first'] == 1)
		self.assertTrue(resp['markup'][0]['group']['last'] == 4)


if __name__ == '__main__':
	unittest.main()

