#!/bin/bash

function sql() { docker exec -it iqass-db psql -U postgres hhdb -c "$*;"; }

set -e
docker rm -f iqass-db || true
docker run --name iqass-db -p5432:5432 -e POSTGRES_PASSWORD=123 -d postgres
sleep 7
docker exec -it iqass-db createdb -U postgres hhdb

sql "DROP TABLE employer" || true
sql "DROP TABLE vacancy" || true
sql "
    CREATE TABLE employer (id int, area int, name varchar, ts timestamp, js jsonb);
"
sql "
    CREATE TABLE vacancy (id int, eid int, closed_by timestamp, ts timestamp, js jsonb);
"




