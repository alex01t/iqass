import psycopg2, json
import logging
from pprint import pprint as p

try:
    connect_str = "dbname='hhdb' user='postgres' host='postgres' password='123'"
    conn = psycopg2.connect(connect_str)
except Exception as e:
    logging.warning(e)
    pass


def get_employers(area):
    logging.info("reading employers for area " + str(area) + "...")
    emps = dict()
    try:
        c = conn.cursor()
        c.execute("""
            select e.js
            from employer e,
            (select id, max(ts) ts from employer where area = %s group by id) m
            where e.area = %s and e.id = m.id and e.ts = m.ts
        """, (area,area,))
        for row in c.fetchall():
            d = row[0]
            emps[d["id"]] = d

    except Exception as e:
        logging.warning(e)

    logging.info("got " + str(len(emps)) + " emplolyers")
    return emps


def set_employers(emps, area):
    logging.info("saving " + str(len(emps)) + " employers for area " + str(area))
    try:
        c = conn.cursor()
        for e in emps:
            c.execute("insert into employer values(%s, %s, %s, %s, now(), %s)",
                           (e["id"], area, e["name"], e["open_vacancies"], json.dumps(e)))

        conn.commit()
    except Exception as e:
        logging.warning(e)

    logging.info("saved")



def set_vacancies(vs):
    try:
        c = conn.cursor()
        for v in vs:
            c.execute(
                "insert into vacancy values(%s, now(), %s)",
                (v["id"], json.dumps(v),)
            )

        conn.commit()
    except Exception as e:
        logging.warning(e)

