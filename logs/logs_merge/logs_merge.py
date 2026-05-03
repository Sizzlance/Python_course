from datetime import datetime
import unittest
from unittest.mock import mock_open, patch


def merge(*iterables, key=None):
    """Функция склеивает упорядоченные по ключу `key` и порядку «меньше»
    коллекции из `iterables`.

    Результат — итератор на упорядоченные данные.
    В случае равенства данных следует их упорядочить в порядке следования
    коллекций"""
    iterators = [iter(it) for it in iterables]
    current_values = []

    for idx, it in enumerate(iterators):
        try:
            current_values.append((next(it), idx))
        except StopIteration:
            pass

    while current_values:
        current_values.sort(key=lambda x: (key(x[0]) if key else x[0], x[1]))
        value, idx = current_values.pop(0)
        yield value
        try:
            current_values.append((next(iterators[idx]), idx))
        except StopIteration:
            pass


def log_key(log_line):
    """Функция по строке лога возвращает ключ для её сравнения по времени"""
    try:
        timestamp = log_line.split("[")[1].split("]")[0]
        return datetime.strptime(timestamp, "%d/%b/%Y:%H:%M:%S %z")
    except (IndexError, ValueError):
        raise ValueError(f"Неверный формат строки лога: {log_line}")


def load_and_sort_logs(filepath, key):
    with open(filepath, "r", encoding="utf-8") as file:
        logs = [line.strip() for line in file]
    logs.sort(key=key)
    return logs


def main():
    input_files = ["example_1.log", "example_2.log", "example_3.log"]
    output_file = "output.log"

    sorted_log_generators = [
        iter(load_and_sort_logs(filepath, key=log_key))
        for filepath in input_files
    ]

    merged_logs = merge(*sorted_log_generators, key=log_key)

    with open(output_file, "w", encoding="utf-8") as output:
        for log in merged_logs:
            output.write(log + "\n")

    print(f"Логи объединены и сохранены в {output_file}")


class TestLogProcessor(unittest.TestCase):
    def test_log_key_valid(self):
        log_line = (
            '192.168.12.10 - - [17/Feb/2013:06:37:21 +0600] '
            '"GET /tv/useUser HTTP/1.1" 200 432'
        )
        expected_datetime = datetime(2013, 2, 17, 6, 37, 21)

        self.assertEqual(
            log_key(log_line).replace(tzinfo=None),
            expected_datetime.replace(tzinfo=None),
        )

    def test_log_key_invalid_format(self):
        log_line = (
            '192.168.12.10 - - [invalid timestamp] '
            '"GET /tv/useUser HTTP/1.1" 200 432'
        )
        with self.assertRaises(ValueError):
            log_key(log_line)

    @patch(
        "builtins.open", mock_open(
            read_data="192.168.12.10 - - [17/Feb/2013:06:37:21 +0600] "
            '"GET /tv/useUser HTTP/1.1"'))
    def test_load_and_sort_logs(self):
        logs = load_and_sort_logs("test.log", key=log_key)
        self.assertEqual(len(logs), 1)
        self.assertIn("17/Feb/2013:06:37:21", logs[0])

    def test_merge(self):
        logs_1 = [
            '192.168.12.10 - - [17/Feb/2013:06:37:21 +0600] '
            '"GET /tv/useUser HTTP/1.1" 200 432',
            '192.168.12.10 - - [18/Feb/2013:06:37:21 +0600] '
            '"GET /tv/useUser HTTP/1.1" 200 432',
        ]
        logs_2 = [
            '192.168.12.108 - - [17/Feb/2013:06:37:21 +0600] '
            '"GET /tv/useUser HTTP/1.1" 200 432',
            '192.168.12.108 - - [18/Feb/2013:06:37:21 +0600] '
            '"GET /tv/useUser HTTP/1.1" 200 432',
        ]

        merged = list(merge(logs_1, logs_2, key=log_key))

        self.assertEqual(merged[0], logs_1[0])
        self.assertEqual(merged[1], logs_2[0])
        self.assertEqual(merged[2], logs_1[1])
        self.assertEqual(merged[3], logs_2[1])


if __name__ == "__main__":
    unittest.main()
