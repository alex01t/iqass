import fetch
from random import randint
from pprint import pprint as p


def test_crawl():
    for i in range(42):
        mock_items = list(map(str, range(randint(0, i * 1000))))

        def mock(page, per):
            url = "...?per_page=" + str(per) + "&page=" + str(page)
            print(url)
            return mock_items[per * page:per * (page + 1)]

        res = fetch.crawl(mock)

        assert len(list(res)) == len(mock_items)


def test_crawl2():
    for i in range(42):
        # mock_items = list(map(lambda x: {"v": x}, range(randint(0, i * 1000))))
        mock_items = []
        mock_items.append(
            map(lambda x: {"v": x}, range(255))
        )

        def mock_get(url):
            per, page = url["per"], url["page"]
            print("url = " + str(url))
            return mock_items[per * page:per * (page + 1)]

        fetch.GETF = mock_get

        urlf = lambda page, per: {"page": page, "per": per}
        res = fetch.crawl2(urlf)

        assert len(list(res)) == len(mock_items)


def test_wget():
    try:
        fetch.wget("https://api.hh.ru/vacancies?per_page=1000&page=42")
    except IndexError:
        pass

    data = fetch.wget("https://api.hh.ru/vacancies?per_page=10&page=0")
    assert len(data) != 0


def f():
    #for empl in [1876072, 1304, 2277549]:
        # vacf = lambda page, per: "https://api.hh.ru/vacancies?employer_id="+str(empl)+ "&page=" + str(page) + "&per_page=" + str(per) + "&area=2"
        # res = list(fetch.crawl2(vacf))

    pass
    for area in [52]:
        res = []
        for emp_type in ["company", "agency", "private_recruiter"]:
            empf = lambda page, per: \
                "https://api.hh.ru/employers?"+\
                "&type="+emp_type+\
                "&only_with_vacancies=true"+ \
                "&area=" + str(area) +\
                "&page=" + str(page) + "&per_page=" + str(per)

            out = list(fetch.crawl2(empf))
            p(len(
                set(map(lambda i: i["id"], out))
            ))
            p(len(out))
            res += out

        p(len(
            set(map(lambda i: i["id"], res))
        ))
        p(len(res))


if __name__ == "__main__":
    test_crawl2()
    test_wget()
