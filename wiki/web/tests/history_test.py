"""
history_test.py
Author: Sam Hogan
CSC440
"""

import unittest
from wiki.web.history import update_history, get_history_id, format_history_id, get_date_from_id

class MySearchTest(unittest.TestCase):
    """
        Test cases for history methods
    """
    def test_givenFileName_whenGetHistoryIDCalled_returnsHID(self):
        self.assertEqual("2020-04-16-15-15-23", get_history_id("2020-04-16-15-15-23.md"))

    def test_givenHID_whenGetDateCalled_returnsDate(self):
        self.assertEqual("2020-04-16-15-15-23", get_date_from_id("2020-04-16-15-15-23"))

    def test_givenHID_whenFormatHIDCalled_returnsFormattedDate(self):
        self.assertEqual("2020-04-16 15:15:23", format_history_id("2020-04-16-15-15-23"))

    def test_givenHIDwithLeadingTime0_whenFormatHIDCalled_returnsFormattedDate(self):
        self.assertEqual("2020-04-16 5:15:23", format_history_id("2020-04-16-05-15-23"))
