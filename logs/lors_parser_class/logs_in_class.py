import unittest
import re
import sys
from collections import Counter
from datetime import datetime


def make_stat():
    class Stat_maker():

        def __init__(self, file_name):
            self.file_name = file_name
            self.Pattern = (
                r"(?P<IP>(\d{1,3}\.){3}\d{1,3})\s+-\s+-\s+"
                r"\[(?P<TIMESTAMP>[^\]]*)\]\s+"
                r'"(?P<REQUEST>[^"]*)"\s+(?P<STATUS>\d+)\s+(?P<SIZE>\d+)\s+'
                r'"(?P<REFERRER>[^"]*)"\s+"(?P<USER_AGENT>[^"]*)"\s+'
                r'(?P<PROCESS_TIME>\d+)'
            )
            self.Log_Re = re.compile(self.Pattern)

        def choose_stat(self, flag):
            if flag == '-c':
                return self.find_most_active_client()
            if flag == '-avgc':
                return self.find_most_active_client_by_day()
            if flag == '-r':
                return self.find_most_popular_resource()
            if flag == '-sr':
                return self.find_slowest_resource()
            if flag == '-fr':
                return self.find_fastest_resource()
            if flag == '-avgsr':
                return self.find_avg_slowest_resource()
            if flag == '-b':
                return self.find_most_popular_browser()

        def parse_str(self, line, arg):
            match = re.search(self.Pattern, line)
            if match:
                if arg == "resource":
                    resource = match.group("REFERRER")
                    arg = resource
                if arg == "ip":
                    ip = match.group("IP")
                    arg = ip
                if arg == "volume":
                    volume = match.group("PROCESS_TIME")
                    arg = volume
                if arg == "browser":
                    browser = match.group("USER_AGENT")
                    arg = browser
                if arg == "timestamp":
                    browser = match.group("TIMESTAMP")
                    arg = browser
                return arg

            return None

        def find_most_popular_resource(self):
            resource_counter = Counter()
            with (open(self.file_name, "r") as f):
                for line in f:
                    resource = self.parse_str(line, "resource")
                    if resource:
                        resource_counter[resource] += 1
                most_popular_res = str(resource_counter.most_common(1)[0][0])
                most_popular_res_count = \
                    int(resource_counter.most_common(1)[0][1])
                for res in range(1, len(resource_counter)):
                    if most_popular_res >= \
                            resource_counter.most_common()[res][0] \
                            and most_popular_res_count == int(
                            resource_counter.most_common()[res][1]):
                        most_popular_res = \
                            str(resource_counter.most_common()[res][0])
                        most_popular_res_count = \
                            int(resource_counter.most_common()[res][1])
            return most_popular_res

        def find_most_active_client(self):
            ip_counter = Counter()
            with open(self.file_name, "r") as f:
                for line in f:
                    ip = self.parse_str(line, "ip")
                    if ip:
                        ip_counter[ip] += 1
                most_active_client = ip_counter.most_common(1)[0][0]
                most_active_client_count = ip_counter.most_common(1)[0][1]
                for ip in range(1, len(ip_counter)):
                    if most_active_client >= ip_counter.most_common()[ip][0] \
                            and most_active_client_count == \
                            ip_counter.most_common()[ip][1]:
                        most_active_client = ip_counter.most_common()[ip][0]
                        most_active_client_count = \
                            ip_counter.most_common()[ip][1]
            return most_active_client

        def find_most_popular_browser(self):
            browser_counter = Counter()
            with (open(self.file_name, "r") as f):
                for line in f:
                    browser = self.parse_str(line, "browser")
                    if browser:
                        browser_counter[browser] += 1
                most_popular_browser = browser_counter.most_common(1)[0][0]
                most_popular_browser_count = \
                    browser_counter.most_common(1)[0][1]
                for browser in range(1, len(browser_counter)):
                    if most_popular_browser >= \
                            browser_counter.most_common()[browser][0] \
                            and most_popular_browser_count == \
                            browser_counter.most_common()[browser][1]:
                        most_popular_browser = \
                            browser_counter.most_common()[browser][0]
                        most_popular_browser_count = \
                            browser_counter.most_common()[browser][1]
            return most_popular_browser

        def find_avg_slowest_resource(self):
            resource_count = {}
            resource_time = {}
            with open(self.file_name, "r") as f:
                for line in f:
                    resource = self.parse_str(line, "resource")
                    volume = self.parse_str(line, "volume")
                    if resource:
                        if resource not in resource_count:
                            resource_count[resource] = 0
                            resource_time[resource] = 0
                        resource_count[resource] += 1
                        resource_time[resource] += int(volume)

            slowest_avg_time = 0
            slowest_avg_resource = ''
            for resource, time in resource_time.items():
                avg_time = time / resource_count[resource]
                if slowest_avg_time < avg_time:
                    slowest_avg_time = avg_time
                    slowest_avg_resource = resource
                elif avg_time == slowest_avg_time and \
                        slowest_avg_resource == '':
                    slowest_avg_resource = resource
            return slowest_avg_time, slowest_avg_resource

        def find_slowest_resource(self):
            with open(self.file_name, "r") as f:
                slowest_current_volume = 0
                slowest_current_res = ''
                for line in f:
                    resource = self.parse_str(line, "resource")
                    volume = self.parse_str(line, "volume")
                    if resource:
                        if int(volume) >= slowest_current_volume:
                            slowest_current_volume = int(volume)
                            slowest_current_res = resource
            return slowest_current_volume, slowest_current_res

        def find_fastest_resource(self):
            with open(self.file_name, "r") as f:
                fastest_current_volume = sys.maxsize
                fastest_current_res = ''
                for line in f:
                    resource = self.parse_str(line, "resource")
                    volume = self.parse_str(line, "volume")
                    if resource:
                        if int(volume) <= fastest_current_volume:
                            fastest_current_volume = int(volume)
                            fastest_current_res = resource
            return fastest_current_volume, fastest_current_res

        def find_most_active_client_by_day(self):
            day_client_counter = {}
            with open(self.file_name, "r") as f:
                for line in f:
                    timestamp = self.parse_str(line, "timestamp")
                    ip = self.parse_str(line, "ip")
                    if timestamp and ip:
                        date = timestamp.split(':')[0]
                        if date not in day_client_counter:
                            day_client_counter[date] = Counter()
                        day_client_counter[date][ip] += 1

            for date, counter in day_client_counter.items():
                most_common = counter.most_common()
                max_count = most_common[0][1]
                most_active_client = \
                    min([ip for ip, count in most_common
                         if count == max_count])
                date = datetime.strptime(date, "%d/%b/%Y")
                formated_date = date.strftime("%d.%m.%Y")
                return formated_date, most_active_client

    file_name = 'example_1.log'
    return Stat_maker(file_name)


class LogStatTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.stat = make_stat()

    def test_find_most_active_client(self):
        expected = "192.168.74.151"
        result = self.stat.find_most_active_client()
        self.assertEqual(result, expected,
                         f"Expected {expected}, got {result}")

    def test_find_most_popular_resource(self):
        expected = "http://callider/pause/index"
        result = self.stat.find_most_popular_resource()
        self.assertEqual(result, expected,
                         f"Expected {expected}, got {result}")

    def test_find_slowest_resource(self):
        expected = (8554988, 'http://callider.kontur/pause/index')
        result = self.stat.find_slowest_resource()
        self.assertEqual(result, expected,
                         f"Expected {expected}, got {result}")

    def test_find_fastest_resource(self):
        expected = (255, 'http://callider/site/index')
        result = self.stat.find_fastest_resource()
        self.assertEqual(result, expected,
                         f"Expected {expected}, got {result}")

    def test_find_avg_slowest_resource(self):
        expected = (273474.75, 'http://callider/')
        result = self.stat.find_avg_slowest_resource()
        self.assertEqual(result, expected,
                         f"Expected {expected}, got {result}")

    def test_find_most_popular_browser(self):
        expected = ("Mozilla/4.0 (compatible; MSIE 7.0;"
                    " Windows NT 6.1; WOW64; Trident/5.0;"
                    " SLCC2; .NET CLR 2.0.50727; .NET CLR 3.5.30729;"
                    " .NET CLR 3.0.30729; Media Center PC 6.0; InfoPath.3;"
                    " .NET4.0C; .NET4.0E)")
        result = self.stat.find_most_popular_browser()
        self.assertEqual(result, expected,
                         f"Expected {expected}, got {result}")


if __name__ == "__main__":
    unittest.main()
