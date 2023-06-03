#!/bin/bash

rm database.db
./gen_json.sh > test.json
./entropydb.py
echo "explain query plan SELECT value,COUNT(value) FROM datapoints WHERE key=? GROUP BY value" | sqlite3 database.db
#for i in $(seq 1 100); do ./gen_json.sh > test.json  ; done # takes about 3 seconds
for i in $(seq 1 100); do ./gen_json.sh > test.json ; ./entropydb.py ; done
