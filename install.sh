#!/bin/bash

function sql() { docker exec -it iqass-db psql -U postgres hhdb -c "$*;"; }

set -e
docker rm -f iqass-db || true
docker run --name iqass-db -p5432:5432 -e POSTGRES_PASSWORD=123 -d postgres
sleep 3
docker exec -it iqass-db createdb -U postgres hhdb

sql "DROP TABLE employer" || true
sql "
    CREATE TABLE employer (id int, area int, name varchar, open_vacancies int, ts timestamp, js jsonb);
"
sql "
    CREATE TABLE vacancy (id int, ts timestamp, js jsonb);
"
sql "
    select l.*
    from employer l
    left join employer r on l.id=r.id and l.ts<r.ts
    where r.id is null;
"
sql "
    select e.*
    from employer e,
    (select id, max(ts) ts from employer group by id) m
    where e.id = m.id and e.ts = m.ts
"






