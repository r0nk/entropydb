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
    cursor.execute("pragma optimize;")
    conn.commit()
    conn.close()

def add_occurrence(cursor,uid,key,value):
    cursor.execute('INSERT OR IGNORE INTO datapoints VALUES (?, ?, ?)', (uid, key, value))

#https://en.wikipedia.org/wiki/Entropy_(information_theory)
#Getting them both with one call is more efficent
def get_entropy_surprisal(cursor,key,value):
    entropy = 0
    cursor.execute("SELECT value,COUNT(value),COUNT(*) FROM datapoints WHERE key=? GROUP BY value", (key,))
    for row in cursor:
        count = row[1]
        total = row[2]
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
    ret = {}
    ret["key_entropy_surprisal"]=[]
    conn = sqlite3.connect('database.db')
    cursor = conn.cursor()
    for kpair in data["kpairs"]:
        add_occurrence(cursor,data["uid"],kpair["key"],kpair["value"])
        e,s =get_entropy_surprisal(cursor,kpair["key"],kpair["value"])
        ret["key_entropy_surprisal"].append([kpair["key"],e,s])
    conn.commit()
    conn.close()
    return ret

@app.route('/', methods=['POST'])
def handle_post():
    start_time=time.time()
    data = request.get_json()
    return handle_data(data)

def test():
    with open('test.json', 'r') as f:
            data = json.load(f)
    start_time=time.time()
    print('starting test...')
    for i in range(100):
        handle_data(data)
    print("total test time:",time.time()-start_time," seconds")

if __name__ == "__main__":
    initalize_table()
    test()
#    app.run()
