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
    conn.commit()
    conn.close()

def add_occurrence(uid,key,value):
    conn = sqlite3.connect('database.db')
    cursor = conn.cursor()

    cursor.execute('INSERT OR IGNORE INTO datapoints VALUES (?, ?, ?)', (uid, key, value))

    conn.commit()
    conn.close()

#https://en.wikipedia.org/wiki/Entropy_(information_theory)
def get_surprisal(key,value):
    conn = sqlite3.connect('database.db')
    cursor = conn.cursor()

    cursor.execute("SELECT COUNT(*) FROM datapoints WHERE key=? AND value=?", (key,value))
    matching = cursor.fetchone()[0]

    cursor.execute("SELECT COUNT(*) FROM datapoints WHERE key=? ", (key,))
    total = cursor.fetchone()[0]

    conn.commit()
    conn.close()
    if(total==0 or matching==0) or ( (matching==total) and (total==1) ):
        return 1
    return math.log2(1/(matching/total))

#TODO fix bottleneck in here
def get_entropy(key):
    conn = sqlite3.connect('database.db')
    cursor = conn.cursor()

    cursor.execute("SELECT COUNT(*) FROM datapoints WHERE key=? ", (key,))
    total = cursor.fetchone()[0]
    if(total==0):
        return 1
    entropy = 0

    cursor.execute("SELECT value,COUNT(value) FROM datapoints WHERE key=? GROUP BY value", (key,))
    for row in cursor:
        count = row[1]
        px=count/total
        entropy-=px*math.log2(px)

    conn.commit()
    conn.close()
    return entropy

app = Flask(__name__)

@app.route('/', methods=['POST'])
def handle_data():
    start_time=time.time()
    data = request.get_json()
    ret = {}
    ret["key_entropy_surprisal"]=[]
    for kpair in data["kpairs"]:
        add_occurrence(data["uid"],kpair["key"],kpair["value"])
        ret["key_entropy_surprisal"].append([kpair["key"],
                                       get_entropy(kpair["key"]),
                                       get_surprisal(kpair["key"],kpair["value"])])
    print("total request time:",time.time()-start_time," seconds")
    return ret

def test():
    start_time=time.time()
    with open('test.json', 'r') as f:
            data = json.load(f)
    ret = {}
    ret["key_entropy_surprisal"]=[]
    for kpair in data["kpairs"]:
        e=get_entropy(kpair["key"])
        s=get_surprisal(kpair["key"],kpair["value"])
        add_occurrence(data["uid"],kpair["key"],kpair["value"])
        ret["key_entropy_surprisal"].append([kpair["key"],e,s])
    print("total request time:",time.time()-start_time," seconds")
    return ret


if __name__ == "__main__":
    initalize_table()
#    test()
    app.run()
