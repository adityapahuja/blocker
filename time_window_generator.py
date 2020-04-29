#!/usr/bin/env python

from datetime import datetime, timedelta, time

from day import Day
from window import Window

__author__ = "Aditya Pahuja"
__copyright__ = "Copyright (c) 2020"

__maintainer__ = "Aditya Pahuja"
__email__ = "aditya.s.pahuja@gmail.com"
__status__ = "Production"


class TimeWindowGenerator:
    def __init__(self, days, start_time, stop_time, time_zone):
        self.days = set()
        for day in days:
            self.days.add(Day[day].value)
        self.start_time = start_time
        self.stop_time = stop_time
        self.time_zone = time_zone

    def get_window_of_time(self, current_date):
        if current_date.weekday() in self.days:
            current_time = time(current_date.hour, current_date.minute, current_date.second, current_date.microsecond, self.time_zone)
            if current_time > self.stop_time:
                return self.get_next_window_of_time(current_date)
            else:
                return self.get_today_window_of_time(current_date)
        else:
            return self.get_next_window_of_time(current_date)

    def get_next_window_of_time(self, window_date):
        window_date = window_date + timedelta(1)
        while window_date.weekday() not in self.days:
            window_date = window_date + timedelta(1)
        return self.get_today_window_of_time(window_date)

    def get_today_window_of_time(self, window_date):
        window_start_date = datetime(window_date.year, window_date.month, window_date.day,
                                     self.start_time.hour, self.start_time.minute, self.start_time.second,
                                     self.start_time.microsecond)
        window_start_date = self.time_zone.localize(window_start_date, is_dst=True)
        window_stop_date = datetime(window_date.year, window_date.month, window_date.day,
                                    self.stop_time.hour, self.stop_time.minute, self.stop_time.second,
                                    self.stop_time.microsecond)
        window_stop_date = self.time_zone.localize(window_stop_date, is_dst=True)
        return Window(window_start_date, window_stop_date)
