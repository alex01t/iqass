from pprint import pprint as p

"""" crawler starts from this value as number of items per page when fetching """
PER_PAGE_INIT = 2**6


def get(url):
    import json
    js = json.loads(wget(url))
    p(url)
    # p(js)
    if "items" in js:
        return js["items"]
    else:
        raise LookupError()


""" GETF is a function which rets an url and returns items """
GETF = get


""" crawl2 receives some function which returns an url based on $page & $per arguments, 
    yields items """
def crawl2(urlf):
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
                print("failed!")
                break


def wget(url):
    import urllib.request, http
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
