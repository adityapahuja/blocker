#!/usr/bin/env python

import unittest
from datetime import datetime, time
import pytz

from time_window_generator import TimeWindowGenerator

__author__ = "Aditya Pahuja"
__copyright__ = "Copyright (c) 2020"

__maintainer__ = "Aditya Pahuja"
__email__ = "aditya.s.pahuja@gmail.com"
__status__ = "Production"


class TestTimeWindowGenerator(unittest.TestCase):
    LONDON_TIMEZONE = pytz.timezone('Europe/London')

    def setUp(self):
        start_time = time(8, 0, 0, 0, TestTimeWindowGenerator.LONDON_TIMEZONE)
        stop_time = time(16, 30, 0, 0, TestTimeWindowGenerator.LONDON_TIMEZONE)
        self.time_checker = TimeWindowGenerator({'MONDAY', 'TUESDAY'}, start_time, stop_time, TestTimeWindowGenerator.LONDON_TIMEZONE)

    def test_get_today_window_when_current_date_is_before_start_time(self):
        date = TestTimeWindowGenerator.LONDON_TIMEZONE.localize(datetime(2020, 1, 6, 7, 59, 59, 999999), is_dst=True)
        window = self.time_checker.get_window_of_time(date)
        self.assertEqual(window.start_date, TestTimeWindowGenerator.LONDON_TIMEZONE.localize(datetime(2020, 1, 6, 8, 0, 0, 0), is_dst=True))
        self.assertEqual(window.stop_date, TestTimeWindowGenerator.LONDON_TIMEZONE.localize(datetime(2020, 1, 6, 16, 30, 0, 0), is_dst=True))

    def test_get_today_window_when_current_date_is_before_end_time(self):
        date = TestTimeWindowGenerator.LONDON_TIMEZONE.localize(datetime(2020, 1, 6, 16, 30, 0, 0), is_dst=True)
        window = self.time_checker.get_window_of_time(date)
        self.assertEqual(window.start_date, TestTimeWindowGenerator.LONDON_TIMEZONE.localize(datetime(2020, 1, 6, 8, 0, 0, 0), is_dst=True))
        self.assertEqual(window.stop_date, TestTimeWindowGenerator.LONDON_TIMEZONE.localize(datetime(2020, 1, 6, 16, 30, 0, 0), is_dst=True))

    def test_get_tomorrow_window_when_current_date_is_after_end_time(self):
        date = TestTimeWindowGenerator.LONDON_TIMEZONE.localize(datetime(2020, 1, 6, 16, 31, 0, 0), is_dst=True)
        window = self.time_checker.get_window_of_time(date)
        self.assertEqual(window.start_date, TestTimeWindowGenerator.LONDON_TIMEZONE.localize(datetime(2020, 1, 7, 8, 0, 0, 0), is_dst=True))
        self.assertEqual(window.stop_date, TestTimeWindowGenerator.LONDON_TIMEZONE.localize(datetime(2020, 1, 7, 16, 30, 0, 0), is_dst=True))

    def test_get_next_window_when_current_date_is_after_end_time_and_is_on_tuesday(self):
        date = TestTimeWindowGenerator.LONDON_TIMEZONE.localize(datetime(2020, 1, 7, 16, 31, 0, 0), is_dst=True)
        window = self.time_checker.get_window_of_time(date)
        self.assertEqual(window.start_date, TestTimeWindowGenerator.LONDON_TIMEZONE.localize(datetime(2020, 1, 13, 8, 0, 0, 0), is_dst=True))
        self.assertEqual(window.stop_date, TestTimeWindowGenerator.LONDON_TIMEZONE.localize(datetime(2020, 1, 13, 16, 30, 0, 0), is_dst=True))

    def test_get_next_window_when_current_date_is_not_on_days(self):
        date = TestTimeWindowGenerator.LONDON_TIMEZONE.localize(datetime(2020, 1, 8, 17, 31, 0, 0), is_dst=True)
        window = self.time_checker.get_window_of_time(date)
        self.assertEqual(window.start_date, TestTimeWindowGenerator.LONDON_TIMEZONE.localize(datetime(2020, 1, 13, 8, 0, 0, 0), is_dst=True))
        self.assertEqual(window.stop_date, TestTimeWindowGenerator.LONDON_TIMEZONE.localize(datetime(2020, 1, 13, 16, 30, 0, 0), is_dst=True))
