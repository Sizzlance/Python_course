import unittest
from logs_classes import Stat_maker

file_name = 'example_1.log'

EXPECTED_RESULTS = {
    "avgc": ('17.02.2013', '192.168.74.151'),
    "-c": "192.168.74.151",
    "-r": "http://callider/pause/index",
    "-sr": (8554988, 'http://callider.kontur/pause/index'),
    "-fr": (255, 'http://callider/site/index'),
    "-avgsr": (273474.75, 'http://callider/'),
    "-b": "Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 6.1;"
          " WOW64; Trident/5.0; SLCC2;"
          " .NET CLR 2.0.50727; .NET CLR 3.5.30729; .NET CLR 3.0.30729;"
          " Media Center PC 6.0; InfoPath.3; .NET4.0C; .NET4.0E)"
}


class TestStatMaker(unittest.TestCase):
    def setUp(self):

        self.temp_file = 'example_1.log'
        self.stat = Stat_maker(self.temp_file)

    def test_find_most_active_client(self):
        with (open(self.temp_file, "r") as f):
            self.assertEqual(self.stat.find_most_active_client(),
                             EXPECTED_RESULTS["-c"])

    def test_find_most_popular_resource(self):
        with (open(self.temp_file, "r") as f):
            self.assertEqual(self.stat.find_most_popular_resource(),
                             EXPECTED_RESULTS["-r"])

    def test_find_slowest_resource(self):
        with (open(self.temp_file, "r") as f):
            self.assertEqual(self.stat.find_slowest_resource(),
                             EXPECTED_RESULTS["-sr"])

    def test_find_fastest_resource(self):
        with (open(self.temp_file, "r") as f):
            self.assertEqual(self.stat.find_fastest_resource(),
                             EXPECTED_RESULTS["-fr"])

    def test_find_avg_slowest_resource(self):
        with (open(self.temp_file, "r") as f):
            self.assertEqual(self.stat.find_avg_slowest_resource(),
                             EXPECTED_RESULTS["-avgsr"])

    def test_find_most_popular_browser(self):
        with (open(self.temp_file, "r") as f):
            self.assertEqual(self.stat.find_most_popular_browser(),
                             EXPECTED_RESULTS["-b"])


if __name__ == "__main__":
    unittest.main()
