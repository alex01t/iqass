import psycopg2, json
import logging
from pprint import pprint as p

try:
    connect_str = "dbname='hhdb' user='postgres' host='postgres' password='123'"
    conn = psycopg2.connect(connect_str)
except Exception as e:
    logging.warning(e)


def get_closed_vacancies():
    return []


def get_employers(area):
    emps = dict()
    try:
        c = conn.cursor()
        c.execute("select e.id, e.js from employer e where area = %s", (area,))
        for row in c.fetchall():
            emps[row[0]] = row[1]

    except Exception as e:
        logging.warning(e)

    return emps


def new_employers(emps, area):
    try:
        c = conn.cursor()
        for e in emps:
            c.execute("insert into employer values(%s, %s, %s, now(), %s)",
                           (e["id"], area, e["name"], json.dumps(e)))
        conn.commit()
    except Exception as e:
        logging.warning(e)


def new_vacancies(vs):
    try:
        c = conn.cursor()
        for v in vs:
            c.execute(
                "insert into vacancy values(%s, %s, null, now(), %s)",
                (v["id"], v["employer"]["id"], json.dumps(v),)
            )
        conn.commit()
    except Exception as e:
        logging.warning(e)


def closed_vacancies(ids: [id]):
    try:
        c = conn.cursor()
        for vid in ids:
            c.execute(
                "update vacancy set closed_by = now(), ts = now() where id = %s", (vid,)
            )
        conn.commit()
    except KeyboardInterrupt as e:
        logging.warning(e)


def get_vacancy_ids():
    try:
        c = conn.cursor()
        c.execute(
            "select eid, id from vacancy where closed_by is null"
        )
        yield from c.fetchall()

    except Exception as e:
        logging.warning(e)