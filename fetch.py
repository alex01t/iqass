import logging
from typing import Generator, Callable

"""" crawler starts from this value as number of items per page when fetching """
PER_PAGE_INIT = 2**6


def employers(area: int) -> Generator[dict, None, None]:

    for emp_type in ["company", "agency", "private_recruiter"]:

        yield from crawl2(
            lambda page, per:
                "https://api.hh.ru/employers?" +
                "&type=" + emp_type +
                "&only_with_vacancies=true" +
                "&area=" + str(area) +
                "&page=" + str(page) + "&per_page=" + str(per)
        )


def get(url):
    import json
    js = json.loads(wget(url))
    logging.debug(url)
    if "items" in js:
        return js["items"]
    else:
        raise LookupError()


""" GETF is a function which rets an url and returns items """
GETF = get


Url = str
""" crawl2 receives some function which returns an url based on $page & $per arguments, 
    yields items """
def crawl2(urlf: Callable[[int, int], Url]):
    def per_page():
        n = PER_PAGE_INIT
        while n > 0:
            yield n
            n = n // 2

    def pages(n):
        while True:
            yield n
            n += 1
    got = 0
    for per in per_page():
        from_page = got // per
        for page in pages(from_page):
            try:
                items = GETF(urlf(page, per))
                got += len(items)
                yield from items
                if len(items) < per:
                    return
            except IndexError:
                logging.debug("failed!")
                break


def wget(url):
    import urllib.request, urllib.error, http
    headers = {'User-Agent': 'api-test-agent',}
    req = urllib.request.Request(url, data=None, headers=headers)

    data = b''
    try:
        from time import sleep
        sleep(0.1)
        with urllib.request.urlopen(req) as response:
            while True:
                try:
                    buf = response.read()
                except http.client.IncompleteRead as e:
                    buf = e.partial
                data += buf
                if not buf:
                    break

    except urllib.error.HTTPError as e:
        if e.code == 400:
            raise IndexError
        else:
            raise e

    return data.decode(response.headers.get_content_charset())
