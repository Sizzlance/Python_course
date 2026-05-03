from urllib.request import urlopen
import urllib.parse
import ssl
import re
import unittest


def get_content(name):
    article_name = "_".join(name.split())
    context = ssl.create_default_context()
    url = f"https://ru.wikipedia.org/wiki/{urllib.parse.quote(article_name)}"
    try:
        response = urlopen(url, context=context)
        return response.read().decode("utf-8")

    except urllib.error.URLError:
        return None


def extract_content(page):
    if page is None:
        return 0, 0
    start = '<div class="mw-content-ltr mw-parser-output"'
    start_of_page = page.find(start)
    end_of_page =(page.find
                  ('<div id="catlinks" class="catlinks" data-mw="interface">'))
    return start_of_page + len(start), end_of_page


def extract_links(page, begin, end):
    final_page = page[begin:end]
    all_links = set()
    pattern = re.compile(r'<a\s+href=[\'"]?/wiki/([^\'" >]+)[\'"]?',
                         re.IGNORECASE)
    matches = pattern.findall(final_page)
    for link in matches:
        if ":" not in link and "#" not in link:
            # Декодируем ссылку и добавляем в результат
            all_links.add(urllib.parse.unquote(link))
    return all_links


def find_chain(start, finish):
    final_chain = [start]
    visited_links = set(start)
    reserve = None
    while True:
        page = get_content(start)
        if page is None:
            if reserve:
                start = reserve
                continue
        first_index = extract_content(page)[0]
        last_index = extract_content(page)[1]
        if first_index == -1 or last_index == -1:
            return None
        all_links = extract_links(page, first_index, last_index)
        if not all_links:
            if reserve:
                start = reserve
                continue
            return None
        if finish in all_links:
            final_chain.append(finish)
            visited_links.clear()
            return final_chain
        decoded_links = set()
        for i in all_links:
            decoded_links.add(i)
        next_link = None
        for i in decoded_links:
            if i not in visited_links:
                next_link = i
                break
        if next_link is None:
            if reserve:
                start = reserve
                reserve = None
            else:
                return None
            continue
        reserve = start
        visited_links.add(next_link)
        final_chain.append(next_link)
        start = next_link
    return None

def sum(arg_1, arg_2):
    return arg_1 + arg_2

if __name__ == "__main__":
    import phil_test
    unittest.main(module=phil_test)
