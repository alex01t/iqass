from VacancyBook import VacancyBook
from pprint import pprint as p
from datetime import timedelta

def main():
    s = """
        <html><head>
        <meta charset="UTF-8">
        <style>
            .closed {color: #c00}
            .new {color: #060}
        </style></head>
    """
    s += "<table>"
    s += """<tr>
                <td>event time</td>
                <td>event</td>
                <td>empl</td>
                <td>published at</td>
                <td>vacancy</td>
            </tr>"""
    for eid, ename, id, ts, published_at, event, name in VacancyBook.get_feed():
        s += "<tr class={0}>".format(event)
        s += "<td>{:%Y-%m-%d %H:%M}</td>".format(ts + timedelta(hours=3))
        s += "<td>{0}</td>".format(event)
        s += "<td><a href=http://hh.ru/employer/{0}>{1}</a></td>".format(eid, ename)
        s += "<td>{:%Y-%m-%d %H:%M}</td>".format(published_at)
        s += "<td><a href=https://hh.ru/vacancy/{0}>{1}</a></td>".format(id, name)
        s += "</tr>\n"

    s += "</table>"

    print(s)

if __name__ == "__main__":
        main()
