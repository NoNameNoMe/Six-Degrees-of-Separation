import time
from requests import get
from bs4 import BeautifulSoup
from re import compile
from queue import Queue, LifoQueue


def parse(start_url, end_url, que, times):
    time.sleep(int(times) / 60)
    headers = {
        'User-Agent': 'Chrome/103.0.5060.53'
    }
    html = get(start_url, headers=headers)
    soup = BeautifulSoup(html.content, features="lxml")
    regular = compile(r"^(/wiki/)((?!:).)*$")
    base = "https://en.wikipedia.org"
    for link in soup.find('div', {'id': 'bodyContent'}).find_all('a', href=regular):
        if base + link.attrs['href'] != end_url:
            que.put(base + link.attrs['href'])
        else:
            return 1
    return 0


def work(depth, start_url, end_url, times, visited, path):
    if start_url in visited:
        return 0
    else:
        visited.append(start_url)
        url_que = LifoQueue()
        path[depth] = start_url
        if parse(start_url, end_url, url_que, times) == 1:
            return 1
        else:
            if depth <= 4:
                depth += 1
                for i in range(0, url_que.qsize()):
                    if work(depth, url_que.get(), end_url, times, visited, path) == 1:
                        return 1
            return 0


if __name__ == '__main__':
    start_url = input()
    end_url = input()
    times = input()
    visited = []
    path = ['', '', '', '', '', '']
    if work(0, start_url, end_url, times, visited, path) == 0:
        print("NOT FIND!")
    else:
        for url in path:
            if url != '':
                print(url + " --> ")
        print(end_url)
