from pprint import pprint as p
from typing import Callable, List, Generator, Dict
import fetch, persist
import logging

Area = int
Employer = dict


class EmployerBook:

    areas: List[Area] = [2, ]

    _list: List[Employer] = []
    _dict: Dict[int, Employer] = dict()

    _data_source = fetch.employers

    @staticmethod
    def setDatasource(ds: Callable[[Area], Generator[Employer, None, None]]):
        EmployerBook._data_source = ds

    @staticmethod
    def add(emp):
        EmployerBook._list.append(emp)

    @staticmethod
    def load():
        logging.info("loading employers...")
        for area in EmployerBook.areas:
            emps = persist.get_employers(area)
            EmployerBook._dict.update(emps)

    @staticmethod
    def get_priority_list() -> List[Employer]:
        def priority(e: Employer) -> bool:
            return int(e["id"]) in [42, 1876072, 1304, 86622]

        if not EmployerBook._dict:
            EmployerBook.load()

        return sorted(list(EmployerBook._dict.values()), key=priority, reverse=True)

    @staticmethod
    def update():

        if not EmployerBook._dict:
            EmployerBook.load()

        for area in EmployerBook.areas:
            fresh_list = []
            for e in EmployerBook._data_source(area):
                fresh_list.append(e)

            fresh_dict = dict(map(lambda e: (e["id"], e), fresh_list))

            olds = EmployerBook._dict

            changed = []
            for k,new in fresh_dict.items():
                old = olds.get(k)
                if not old \
                        or old.get("name") != new.get("name") \
                        or old.get("open_vacancies") != new.get("open_vacancies"):

                    changed.append(new)

            EmployerBook._dict.update(fresh_dict)

            persist.set_employers(changed, area)

    @staticmethod
    def clean():
        EmployerBook._dict = dict()

    @staticmethod
    def dump():
        import json
        return json.dumps(list(EmployerBook._dict.values()))


def show():
    import pprint
    sample = EmployerBook.get_priority_list()[:10]
    pprint.pprint(sample)


def test():

    def fake_datasource(a: Area):
        return [
            {"id": 40, "name": "c40", "open_vacancies": 5},
            {"id": 41, "name": "c41", "open_vacancies": 12},
            {"id": 42, "name": "c42", "open_vacancies": 71},
        ]

    def another_fake_datasource(a: Area):
        return [
            {"id": 41, "name": "c41", "open_vacancies": 12},
            {"id": 42, "name": "c42", "open_vacancies": 69},
        ]

    EmployerBook.areas = [-1]

    EmployerBook.setDatasource(fake_datasource)
    EmployerBook.update()
    show()

    EmployerBook.setDatasource(another_fake_datasource)
    EmployerBook.update()
    show()
    r = EmployerBook.dump()
    p(r)


def real_test():
    logging.basicConfig(level=logging.DEBUG)

    EmployerBook.areas = [54]
    EmployerBook.setDatasource(fetch.employers)

    EmployerBook.update()

    show()


if __name__ == "__main__":

    logging.basicConfig(level=logging.DEBUG)
    test()
    #real_test()
    pass
