import logging, persist
from pprint import pprint as p


class VacancyBook:
    _dict = dict()
    _closed = []

    @staticmethod
    def update(emp_id: int, vs: [dict]):
        fresh = dict(map(lambda v: (int(v["id"]), v), vs))
        old: [int] = VacancyBook._dict.get(emp_id)
        new = []
        closed = []
        if not old:
            new = vs
        else:
            for o in old:
                if o not in fresh:
                    closed.append(o)
            for fk, fv in fresh.items():
                if fk not in old:
                    new.append(fv)

        if new:
            logging.info("saving vacancies: %s", ",".join(map(lambda v: v["id"], new)))
            persist.new_vacancies(new)

        if closed:
            logging.info("closing vacancies: %s", closed)
            persist.closed_vacancies(closed)

        VacancyBook._dict[emp_id] = set(fresh.keys())
        VacancyBook._closed += closed

    @staticmethod
    def load():
        c = 0
        for eid, vid in persist.get_vacancy_ids():
            s = VacancyBook._dict.get(eid, set())
            s.add(vid)
            VacancyBook._dict[eid] = s
            c += 1
        logging.info("loaded %s vacancies for %s employers", c, len(VacancyBook._dict))

    @staticmethod
    def get_feed():
        return persist.get_vacancy_events()

