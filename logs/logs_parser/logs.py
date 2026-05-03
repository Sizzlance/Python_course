import re
import sys
from collections import Counter


Pattern = (
    r"(?P<IP>(\d{1,3}\.){3}\d{1,3})\s+-\s+-\s+\[(?P<TIMESTAMP>[^\]]*)\]\s+"
    r'"(?P<REQUEST>[^"]*)"\s+(?P<STATUS>\d+)\s+(?P<SIZE>\d+)\s+'
    r'"(?P<REFERRER>[^"]*)"\s+"(?P<USER_AGENT>[^"]*)"\s+(?P<PROCESS_TIME>\d+)'
)
Log_Re = re.compile(Pattern)


def parse_file(name, arg):
    referrer_counter = Counter()
    ip_counter = Counter()
    with open(name, "r") as f:
        for line in f:
            ip, referrer = parse_str(line)
            if ip:
                ip_counter[ip] += 1
            if referrer:
                referrer_counter[referrer] += 1
        if arg == "-c":
            print(ip_counter.most_common(1)[0][0])
        if arg == "-r":
            print(referrer_counter.most_common(1)[0][0])


def parse_str(line):
    match = re.search(Pattern, line)
    if match:
        referrer = match.group("REFERRER")
        ip = match.group("IP")
        return ip, referrer
    return None, None


if __name__ == "__main__":
    if len(sys.argv) != 3:
        sys.exit(1)
    file_name = sys.argv[1]
    argument = sys.argv[2]
    parse_file(file_name, argument)
