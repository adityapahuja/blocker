#!/usr/bin/env python

import unittest
from datetime import datetime
from unittest import mock

import pytz

import blocker

__author__ = "Aditya Pahuja"
__copyright__ = "Copyright (c) 2020"

__maintainer__ = "Aditya Pahuja"
__email__ = "aditya.s.pahuja@gmail.com"
__status__ = "Production"


class TestBlocker(unittest.TestCase):
    LONDON_TIMEZONE = pytz.timezone('Europe/London')

    def test_should_throw_error_when_days_are_not_specified(self):
        with self.assertRaises(SystemExit) as em, self.assertRaises(Exception):
            blocker.Blocker.main([])
        self.assertEqual(em.exception.code, 2)

    def test_should_throw_error_when_days_has_an_invalid_day(self):
        invalid_day = 'Mon'
        with self.assertRaises(SystemExit) as em, self.assertLogs('blocker', level='ERROR') as lm:
            blocker.Blocker.main(['-d', invalid_day])
        self.assertEqual(em.exception.code, 1)
        self.assertEqual(lm.output, ["ERROR:blocker:{} is an invalid day. It should be one of "
                                     "['MONDAY', 'TUESDAY', 'WEDNESDAY', 'THURSDAY', 'FRIDAY', 'SATURDAY', 'SUNDAY'] "
                                     "valid days.".format(invalid_day)])

    def test_should_throw_error_when_timezone_is_not_specified(self):
        with self.assertRaises(SystemExit) as em, self.assertRaises(Exception):
            blocker.Blocker.main(['-d', 'Monday', '-t'])
        self.assertEqual(em.exception.code, 2)

    def test_should_throw_error_when_timezone_is_not_valid(self):
        invalid_timezone = 'Europe/NewLondon'
        with self.assertRaises(SystemExit) as em, self.assertLogs('blocker', level='ERROR') as lm:
            blocker.Blocker.main(['-d', 'Monday,Tuesday', '-t', invalid_timezone])
        self.assertEqual(em.exception.code, 1)
        self.assertEqual(lm.output, ["ERROR:blocker:{} is not a valid timezone.".format(invalid_timezone)])

    def test_should_throw_error_when_start_time_is_not_specified(self):
        with self.assertRaises(SystemExit) as em, self.assertRaises(Exception):
            blocker.Blocker.main(['-d', 'Monday', '-s'])
        self.assertEqual(em.exception.code, 2)

    def test_should_throw_error_when_start_time_has_an_invalid_time_format(self):
        invalid_time_format = '08:00:00+00:00'
        with self.assertRaises(SystemExit) as em, self.assertLogs('blocker', level='ERROR') as lm:
            blocker.Blocker.main(['-d', 'Monday', '-s', invalid_time_format])
        self.assertEqual(em.exception.code, 1)
        self.assertEqual(lm.output, ["ERROR:blocker:The start time has an invalid time format [{}]. It should be in "
                                     "%H:%M:%S".format(invalid_time_format)])

    def test_should_throw_error_when_stop_time_is_not_specified(self):
        with self.assertRaises(SystemExit) as em, self.assertRaises(Exception):
            blocker.Blocker.main(['-d', 'Monday', '-e'])
        self.assertEqual(em.exception.code, 2)

    def test_should_throw_error_when_stop_time_has_an_invalid_time_format(self):
        invalid_time_format = '10:00'
        with self.assertRaises(SystemExit) as em, self.assertLogs('blocker', level='ERROR') as lm:
            blocker.Blocker.main(['-d', 'Monday', '-e', invalid_time_format])
        self.assertEqual(em.exception.code, 1)
        self.assertEqual(lm.output, ["ERROR:blocker:The stop time has an invalid time format [{}]. It should be in "
                                     "%H:%M:%S".format(invalid_time_format)])

    def test_should_throw_error_when_start_time_is_greater_than_stop_time(self):
        start_time = '16:31:00'
        stop_time = '16:30:00'
        with self.assertRaises(SystemExit) as em, self.assertLogs('blocker', level='ERROR') as lm:
            blocker.Blocker.main(['-d', 'Monday', '-s', start_time, '-e', stop_time])
        self.assertEqual(em.exception.code, 1)
        self.assertEqual(lm.output, ["ERROR:blocker:The start time [{}] cannot be greater than or equal to the stop time [{}]"
                         .format(start_time, stop_time)])

    def test_should_throw_error_when_start_time_is_equal_to_stop_time(self):
        same_time = '16:30:00'
        with self.assertRaises(SystemExit) as em, self.assertLogs('blocker', level='ERROR') as lm:
            blocker.Blocker.main(['-d', 'Monday', '-s', same_time, '-e', same_time])
        self.assertEqual(em.exception.code, 1)
        self.assertEqual(lm.output, ["ERROR:blocker:The start time [{}] cannot be greater than or equal to the stop time [{}]"
                         .format(same_time, same_time)])

    def test_should_throw_error_when_start_time_is_less_than_2_minutes_from_stop_time(self):
        start_time = '16:28:01'
        stop_time = '16:30:00'
        with self.assertRaises(SystemExit) as em, self.assertLogs('blocker', level='ERROR') as lm:
            blocker.Blocker.main(['-d', 'Monday', '-s', start_time, '-e', stop_time])
        self.assertEqual(em.exception.code, 1)
        self.assertEqual(lm.output, ["ERROR:blocker:The start time [{}] should be at least two minutes from the stop time [{}]"
                         .format(start_time, stop_time)])

    @mock.patch('blocker.Blocker.get_current_date')
    def test_should_allow_you_pass_when_current_time_meets_criteria(self, mock_get_current_date):
        mock_get_current_date.return_value = TestBlocker.LONDON_TIMEZONE.localize(datetime(2020, 4, 27, 16, 28, 0, 0), is_dst=True)
        blocker.Blocker.main(['-d', 'Monday', '-s', '16:28:00', '-e', '16:30:00', '-t', 'Europe/London'])
