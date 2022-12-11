#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2017/12/21 8:49
# @Author  : Aries (i@iw3c.com), KTY
# @Site    : http://iw3c.com
# @File    : time_convertor.py
# @Software: PyCharm
import os
import copy
from typing import List
from enum import Enum
from wox import Wox, WoxAPI
from datetime import datetime, timedelta, timezone

result_template = {
    'Title': '{}: {}',
    'SubTitle': 'copy to clipboard',
    'IcoPath': 'ui/icon.png',
    'JsonRPCAction': {
        'method': 'copy_to_clipboard',
        'parameters': ['{}'],
        'dontHideAfterAction': False
    }
}

LOCAL_TIME = "local time"
TIMESTAMP = "timestamp"


class QueryType(Enum):
    INVALID = "invalid"
    NOW = "now"
    TIMESTAMP = "timestamp"
    DATETIME = "datetime"


class MyTimezone:
    def __init__(self, offset, is_local=False):
        """
        init
        :param offset: offset from utc timezone, unit: hour
        """
        self.offset = offset
        self.timezone = timezone(timedelta(hours=offset))
        if offset == 0:
            self.name = "UTC"
        elif offset > 0:
            self.name = "UTC+" + str(offset)
        else:
            self.name = "UTC" + str(offset)
        self.is_local = is_local

    def get_offset_second(self):
        return self.offset * 3600


class Main(Wox):
    def query(self, key):
        result = []
        query_type, query_subject, timezone_list = self.parse_input(key)

        if query_type == QueryType.NOW:
            now_timestamp = int(datetime.now().timestamp())
            self.add_item(result, TIMESTAMP, now_timestamp)
            time_result = self.format_timestamp(now_timestamp)
            self.add_item(result, LOCAL_TIME, time_result)
            for _timezone in timezone_list:
                time_result = self.format_timestamp(now_timestamp, _timezone.timezone)
                self.add_item(result, _timezone.name, time_result)
        elif query_type == QueryType.TIMESTAMP:
            query_timestamp = self.parse_timestamp(query_subject)
            time_result = self.format_timestamp(query_timestamp)
            self.add_item(result, LOCAL_TIME, time_result)
            for _timezone in timezone_list:
                time_result = self.format_timestamp(query_timestamp, _timezone.timezone)
                self.add_item(result, _timezone.name, time_result)
        elif query_type == QueryType.DATETIME:
            sharp_index = query_subject.find("#")
            if sharp_index != -1:
                query_datetime = query_subject[0: sharp_index]
                from_timezone = MyTimezone(self.get_utc_offset_hour(query_subject[sharp_index + 1:]))
            else:
                query_datetime = query_subject
                from_timezone = None
            time_data = datetime.strptime(query_datetime, "%Y-%m-%d %H:%M:%S")
            time_data = time_data.replace(tzinfo=from_timezone)
            timestamp = int(time_data.timestamp())
            self.add_item(result, TIMESTAMP, timestamp)
            for _timezone in timezone_list:
                time_result = self.format_timestamp(timestamp, _timezone.timezone)
                self.add_item(result, _timezone.name, time_result)
        else:
            self.add_item(result, "unknown pattern", key)

        return result

    def add_item(self, result: List[dict], prefix, value):
        template = copy.deepcopy(result_template)
        template['Title'] = template['Title'].format(prefix, value)
        template['JsonRPCAction']['parameters'][0] = str(value)
        result.append(template)

    def parse_input(self, key: str) -> (str, str, List[MyTimezone]):
        input = key.strip()
        params = input.split(' ')
        if params[0] == "now":
            query_type = QueryType.NOW
            query_subject = "now"
            tzs = params[1:]
        elif self.is_timestamp(params[0]):
            query_type = QueryType.TIMESTAMP
            query_subject = params[0]
            tzs = params[1:]
        elif self.is_datetime(params):
            query_type = QueryType.DATETIME
            query_subject = " ".join([params[0], params[1]])
            tzs = params[2:]
        else:
            query_type = QueryType.INVALID
            query_subject = ""
            tzs = []

        aimed_timezone_list = list()
        for tz in tzs:
            tz = tz.strip()
            if tz.find('#') != -1:
                continue
            if tz.find('utc') == -1:
                continue
            offset_hour = self.get_utc_offset_hour(tz)
            aimed_timezone_list.append(MyTimezone(offset_hour))

        return query_type, query_subject, aimed_timezone_list

    def format_timestamp(self, timestamp: int, _timezone: timezone = None) -> str:
        return datetime.fromtimestamp(timestamp, tz=_timezone).strftime("%Y-%m-%d %H:%M:%S")

    def copy_to_clipboard(self, value):
        command = 'echo ' + str(value).strip() + '| clip'
        os.system(command)

    def is_timestamp(self, value: str) -> bool:
        strlen = len(value)
        if strlen != 10 and strlen != 13:
            return False
        try:
            int(value)
        except:
            return False
        return True

    def is_datetime(self, params):
        if len(params) < 2:
            return False
        dt = " ".join([params[0], params[1]])
        sharp_index = dt.find('#')
        if sharp_index != -1:
            dt = dt[:sharp_index]
        try:
            datetime.strptime(dt, "%Y-%m-%d %H:%M:%S")
        except:
            return False
        return True

    def parse_timestamp(self, value: str) -> int:
        data = int(value)
        strlen = len(value)
        if strlen == 13:
            data = data / 1000.0
        return data

    def get_utc_offset_hour(self, tz):
        return int(tz[3:]) if len(tz) > 3 else 0


if __name__ == '__main__':
    Main()
