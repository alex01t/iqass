#!/usr/bin/python3.6
from pprint import pprint as p
import fetch
import persist
from EmployerBook import EmployerBook
import logging
import time

logging.basicConfig(level=logging.DEBUG)

def d(o):
    import json
    return json.dumps(o)

def main():

    while True:

        """
            remember vacancies in Emp/vs/vac_id dict    a, to check which were removed
            
            no db -- no issue: will just output disappearing items 
        
        """


        for emp in EmployerBook.get_priority_list():
            emp_id = emp["id"]

            vacf = lambda page, per: \
                "https://api.hh.ru/vacancies?" + \
                "&employer_id=" + str(emp_id) + \
                "&page=" + str(page) + "&per_page=" + str(per)

            vs = list(fetch.crawl2(vacf))

            logging.info("got %s vacancies for employer %s", len(vs), emp_id)
            persist.set_vacancies(vs)

        EmployerBook.update()

        logging.info("10s sleep...")
        time.sleep(600)


if __name__ == "__main__":
    main()

