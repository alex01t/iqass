#!/usr/bin/python3.6
from pprint import pprint as p
import fetch
import persist
from EmployerBook import EmployerBook
from VacancyBook import VacancyBook
import logging
import time

logging.basicConfig(level=logging.INFO)

def main():

    EmployerBook.load()
    VacancyBook.load()

    try:
        while True:

            EmployerBook.update()

            for emp in EmployerBook.get_priority_list():
                emp_id = int(emp["id"])

                vacf = lambda page, per: \
                    "https://api.hh.ru/vacancies?" + \
                    "&employer_id=" + str(emp_id) + \
                    "&page=" + str(page) + "&per_page=" + str(per)

                vs = list(fetch.crawl2(vacf))
                logging.debug("got %s vacancies for employer %s", len(vs), emp_id)
                VacancyBook.update(emp_id, vs)

            logging.info("done here, sleep()")
            time.sleep(60)

    except KeyboardInterrupt:
        pass

if __name__ == "__main__":
    main()

