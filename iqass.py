from pprint import pprint as p
import fetch
import persist

def main():
    for area in [52]:
        for emp_type in ["company", "agency", "private_recruiter"]:

            empf = lambda page, per: \
                "https://api.hh.ru/employers?" + \
                "&type=" + emp_type + \
                "&only_with_vacancies=true" + \
                "&area=" + str(area) + \
                "&page=" + str(page) + "&per_page=" + str(per)

            for emp in fetch.crawl2(empf):
                persist.employer(emp)
                emp_id = emp["id"]

                vacf = lambda page, per: \
                    "https://api.hh.ru/vacancies?" + \
                    "&employer_id=" + str(emp_id) + \
                    "&area=" + str(area) + \
                    "&page=" + str(page) + "&per_page=" + str(per)

                vs = []
                for vac in fetch.crawl2(vacf):
                    vs.append(vac)

                persist.vacancies(vs)
                print("empl " + emp_id + " - " + str(len(vs)) + " vacancies")


if __name__ == "__main__":
    main()