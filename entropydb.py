#!/bin/env python3
from flask import Flask, request

import sqlite3
import math
import time
import json

def initalize_table():
    conn = sqlite3.connect('database.db')
    cursor = conn.cursor()
    cursor.execute("CREATE TABLE IF NOT EXISTS datapoints (uid text, key text, value text,UNIQUE(uid,key))")
    cursor.execute("CREATE INDEX IF NOT EXISTS keyindex ON datapoints(key)")
   #cursor.execute("CREATE INDEX IF NOT EXISTS keyvalindex ON datapoints(key,value)")
    cursor.execute("PRAGMA optimize;")
    conn.commit()
    conn.close()

def add_occurrence(cursor,uid,key,value):
    cursor.execute('INSERT OR IGNORE INTO datapoints VALUES (?, ?, ?)', (uid, key, value))

#https://en.wikipedia.org/wiki/Entropy_(information_theory)
#Getting them both with one call is more efficent
def get_entropy_surprisal(cursor,key,value):
    entropy = 0

    total=0

    matching=0
    cursor.execute("SELECT value,COUNT(value) FROM datapoints WHERE key=? GROUP BY value", (key,))
    rows = cursor.fetchall()

    for row in rows:
        total+=row[1]
    for row in rows:
        count = row[1]
        px=count/total
        entropy-=px*math.log2(px)
        if(row[0]==value):
            matching=count

    if(total==0 or matching==0) or ( (matching==total) and (total==1) ):
        surprisal=1
    else:
        surprisal = math.log2(1/(matching/total))

    return entropy, surprisal

app = Flask(__name__)

def handle_data(data):
    start_time=time.time()
    ret = {}
    ret["key_entropy_surprisal"]=[]
    conn = sqlite3.connect('database.db')
    cursor = conn.cursor()
    avg_e=0
    #we separate these loops in order to improve reliability of database writes
    for kpair in data["kpairs"]:
        add_occurrence(cursor,data["uid"],kpair["key"],kpair["value"])
    conn.commit()
    for kpair in data["kpairs"]:
        e,s =get_entropy_surprisal(cursor,kpair["key"],kpair["value"])
        avg_e+=e
        ret["key_entropy_surprisal"].append([kpair["key"],e,s])
    conn.commit()
    conn.close()
    avg_e/=len(data["kpairs"])
    ret["avg_entropy"]=avg_e
    print("[",len(data["kpairs"]),"] request time:",time.time()-start_time," seconds, average entropy:",avg_e,)
    return ret

@app.route('/', methods=['POST'])
def handle_post():
    start_time=time.time()
    data = request.get_json()
    return handle_data(data)

def test():
    with open('test.json', 'r') as f:
            data = json.load(f)
    for i in range(1):
        handle_data(data)

if __name__ == "__main__":
    initalize_table()
#    test()
    app.run()
