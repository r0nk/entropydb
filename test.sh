#!/bin/bash

rm database.db
for i in $(seq 1 100); do ./gen_json.sh > test.json ; ./entropydb.py ; done
