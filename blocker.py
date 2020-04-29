#!/usr/bin/env python

import argparse
import logging
import sys
from datetime import datetime, time
from time import sleep

import pytz

from day import Day
from time_window_generator import TimeWindowGenerator

__author__ = "Aditya Pahuja"
__copyright__ = "Copyright (c) 2020"

__maintainer__ = "Aditya Pahuja"
__email__ = "aditya.s.pahuja@gmail.com"
__status__ = "Production"


class Blocker:
    LOGGER = logging.getLogger('blocker')

    @staticmethod
    def get_days(input_days_string):
        input_days = input_days_string.split(',')
        days = set()
        valid_days = [item.name for item in Day]
        for input_day in input_days:
            uppercase_day = input_day.upper()
            if uppercase_day not in valid_days:
                Blocker.LOGGER.error('%s is an invalid day. It should be one of %s valid days.', input_day, valid_days)
                exit(1)
            else:
                days.add(uppercase_day)
        return days

    @staticmethod
    def get_time(field_name, time_string, timezone):
        try:
            parsed_time = datetime.strptime(time_string, '%H:%M:%S').time()
            return time(parsed_time.hour, parsed_time.minute, parsed_time.second, parsed_time.microsecond, timezone)
        except ValueError:
            Blocker.LOGGER.error('The %s has an invalid time format [%s]. It should be in %%H:%%M:%%S', field_name, time_string)
            exit(1)

    @staticmethod
    def get_timezone(timezone_string):
        if timezone_string in pytz.all_timezones:
            return pytz.timezone(timezone_string)
        else:
            Blocker.LOGGER.error('%s is not a valid timezone.', timezone_string)
            exit(1)

    @staticmethod
    def validate_start_and_stop_times(start_time, stop_time):
        if start_time >= stop_time:
            Blocker.LOGGER.error('The start time [%s] cannot be greater than or equal to the stop time [%s]', start_time, stop_time)
            exit(1)

        time_delta = datetime.combine(datetime.today(), stop_time) - datetime.combine(datetime.today(), start_time)
        if time_delta.total_seconds() < 120:
            Blocker.LOGGER.error('The start time [%s] should be at least two minutes from the stop time [%s]', start_time, stop_time)
            exit(1)

    @staticmethod
    def get_current_date(timezone):
        return datetime.now(timezone)

    @staticmethod
    def parse_args(args):
        parser = argparse.ArgumentParser()
        parser.add_argument('-d',
                            '--days',
                            type=Blocker.get_days,
                            help="Set days where the blocker allows you to pass. For example Monday,Tuesday. "
                                 "The default days are MONDAY,TUESDAY,WEDNESDAY,THURSDAY,FRIDAY.",
                            required=True
                            )
        parser.add_argument('-t',
                            '--timezone',
                            type=Blocker.get_timezone,
                            help="Set the timezone. The default timezone is 'Europe/London'",
                            default=pytz.timezone('Europe/London')
                            )
        parser.add_argument('-s',
                            '--startTime',
                            type=str,
                            help='Set the start time in %H:%M:%S format e.g. 08:00:00. The default start time is 08:00.',
                            default='08:00:00'
                            )
        parser.add_argument('-e',
                            '--stopTime',
                            type=str,
                            help='Set the stop time in %H:%M:%S format e.g. 16:30:00. The default start time is 16:30.',
                            default='16:30:00'
                            )
        return parser.parse_args(args)

    @staticmethod
    def main(args):
        parsed_args = Blocker.parse_args(args)

        start_time = Blocker.get_time('start time', parsed_args.startTime, parsed_args.timezone)
        stop_time = Blocker.get_time('stop time', parsed_args.stopTime, parsed_args.timezone)

        Blocker.validate_start_and_stop_times(start_time, stop_time)

        time_window_generator = TimeWindowGenerator(parsed_args.days, start_time, stop_time, parsed_args.timezone)

        current_date = Blocker.get_current_date(parsed_args.timezone)
        window_date = time_window_generator.get_window_of_time(current_date)
        start_date = window_date.start_date
        stop_date = window_date.stop_date
        while True:
            if start_date <= current_date <= stop_date:
                Blocker.LOGGER.info('Unblock the trigger.')
                break
            Blocker.LOGGER.info('Current time: {} Blocking the trigger until the start time {}'.format(current_date, start_date))
            sleep(60)
            current_date = Blocker.get_current_date(parsed_args.timezone)


if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO)
    Blocker.main(sys.argv[1:])
