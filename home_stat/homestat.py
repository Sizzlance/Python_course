from _operator import itemgetter
from urllib.request import urlopen
import unittest
import urllib
import ssl

context = ssl.create_default_context()
url = "https://alexbers.com/python/home.html"
named_file = "home.html"

with urllib.request.urlopen(url) as response:
    html_content = response.read()

with open(named_file, "wb") as file:
    file.write(html_content)

with open(named_file, "r", encoding="cp1251") as file:
    html_content = file.read()

response = urlopen(url, context=context)


def make_stat(named_file):

    html_str = str(html_content)
    html_str_1 = str(html_content)
    all_years = []  # Массив со всеми годами, которые есть на странице

    while True:
        start_year = html_str.find("<h3>") + 4
        end_year = html_str.find("</h3", start_year)
        all_years.append(html_str[start_year:end_year])
        html_str = html_str[end_year:]
        if html_str.find("<h3") == -1:
            break

    target_year = int(all_years[0])  # Первый год в списке
    full_stat = (
        {}
    )

    while target_year >= int(all_years[-1]):
        if (str(target_year - 1) not in html_str_1 and
                target_year > int(all_years[-1])):
            target_year -= 1
            continue
        if target_year not in full_stat:
            full_stat[target_year] = []
        start = html_str_1.find("/>") + 2
        end = html_str_1.find("<", start)
        if start != -1 and end != -1:
            full_name = html_str_1[start:end]
            name = full_name.split()[1]
            full_stat[target_year].append(name)
            html_str_1 = html_str_1[end:]
        else:
            target_year -= 1
        if html_str_1.find("/>") == -1:
            break

    for i in range(1, len(all_years)):
        full_stat[int(all_years[0]) - i].insert(
            0, full_stat[int(all_years[0]) + 1 - i][-1]
        )
        full_stat[int(all_years[0]) + 1 - i].pop()

    names_counter_by_year = {}
    for all_years in full_stat:
        names_counter = {}
        gender_dict = {}

        for current_name in full_stat[all_years]:
            if current_name not in names_counter:
                names_counter[current_name] = 1
            else:
                names_counter[current_name] += 1

        for current_name in full_stat[all_years]:
            if (
                (
                    current_name[-1] == "а"
                    or current_name[-1] == "я"
                    or current_name == "Любовь"
                )
                and current_name != "Илья"
                and current_name != "Лёва"
                and current_name != "Никита"
            ):
                gender_dict[current_name] = "Девушка"
            else:
                gender_dict[current_name] = "Мужчина"

        men = {
            name: count
            for name, count in names_counter.items()
            if gender_dict.get(name) == "Мужчина"
        }
        women = {
            name: count
            for name, count in names_counter.items()
            if gender_dict.get(name) == "Девушка"
        }

        names_counter_by_year[str(all_years)] =\
            {"Мужчины": men, "Девушки": women}

    return names_counter_by_year


def extract_years(stat):
    return sorted(list(stat.keys()))


def extract_general(stat):
    total_name_counts = {}
    for year_data in stat.values():
        for name, count in year_data["Мужчины"].items():
            total_name_counts[name] = total_name_counts.get(name, 0) + count
        for name, count in year_data["Девушки"].items():
            total_name_counts[name] = total_name_counts.get(name, 0) + count
    sorted_name_stat = sorted(
        total_name_counts.items(), key=itemgetter(1), reverse=True
    )
    return sorted_name_stat


def extract_general_male(stat):
    total_name_counts = {}
    for year_data in stat.values():
        for name, count in year_data["Мужчины"].items():
            total_name_counts[name] = total_name_counts.get(name, 0) + count
    sorted_name_stat = sorted(
        total_name_counts.items(), key=itemgetter(1), reverse=True
    )
    return sorted_name_stat


def extract_general_female(stat):
    total_name_counts = {}
    for year_data in stat.values():
        for name, count in year_data["Девушки"].items():
            total_name_counts[name] = total_name_counts.get(name, 0) + count
    sorted_name_stat = sorted(
        total_name_counts.items(), key=itemgetter(1), reverse=True
    )
    return sorted_name_stat


def extract_year(stat, year):
    total_name_counts = {}
    year_data = stat[year]
    for name, count in year_data["Мужчины"].items():
        total_name_counts[name] = total_name_counts.get(name, 0) + count
    for name, count in year_data["Девушки"].items():
        total_name_counts[name] = total_name_counts.get(name, 0) + count
    sorted_name_stat = sorted(
        total_name_counts.items(), key=itemgetter(1), reverse=True
    )
    return sorted_name_stat


def extract_year_male(stat, year):
    total_name_counts = {}
    year_data = stat[year]
    for name, count in year_data["Мужчины"].items():
        total_name_counts[name] = total_name_counts.get(name, 0) + count
    sorted_name_stat = sorted(
        total_name_counts.items(), key=itemgetter(1), reverse=True
    )
    return sorted_name_stat


def extract_year_female(stat, year):
    total_name_counts = {}
    year_data = stat[year]
    for name, count in year_data["Девушки"].items():
        total_name_counts[name] = total_name_counts.get(name, 0) + count
    sorted_name_stat = sorted(
        total_name_counts.items(), key=itemgetter(1), reverse=True
    )
    return sorted_name_stat



def main():


    stat = make_stat(html_content)
    print(make_stat(html_content))
    print(extract_years(stat))
    print(extract_general(stat))
    print(extract_general_male(stat))
    print(extract_general_female(stat))
    print(extract_year(stat, '2011'))
    print(extract_year_male(stat, '2012'))
    print(extract_year_female(stat, '2006'))

'''
if __name__ == "__main__":
    import test_homestat

    unittest.main(module=test_homestat)
'''

if __name__ == "__main__":
    main()