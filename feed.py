from VacancyBook import VacancyBook
from pprint import pprint as p

def main():
    s = """
        <style>
            .closed {color: #c00}
            .new {color: #060}
        </style>
    """
    s += "<table>"
    s += "<tr><td>ts</td><td>empl</td><td>event</td><td>vacancy</td></tr>"
    for eid, ename, id, ts, event, name in VacancyBook.get_feed():
        s += "<tr class={0}>".format(event)
        s += "<td>{:%Y-%m-%d %H:%M}</td>".format(ts)
        s += "<td><a href=http://hh.ru/employer/{0}>{1}</a></td>".format(eid, ename)
        s += "<td>{0}</td>".format(event)
        s += "<td><a href=https://hh.ru/vacancy/{0}>{1}</a></td>".format(id, name)
        s += "</tr>\n"

    s += "</table>"

    print(s)

if __name__ == "__main__":
    main()