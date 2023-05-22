#!/bin/env python3
from flask import Flask, request

import sqlite3

def initalize_table():
    conn = sqlite3.connect('database.db')
    cursor = conn.cursor()
    cursor.execute("CREATE TABLE IF NOT EXISTS datapoints (uid text, key text, value text,UNIQUE(uid))")
    conn.commit()
    conn.close()

def add_occurrence(uid,key,value):
    conn = sqlite3.connect('database.db')
    cursor = conn.cursor()

    cursor.execute('INSERT OR IGNORE INTO datapoints VALUES (?, ?, ?)', (uid, key, value))

    conn.commit()
    conn.close()

def get_rarity(key,value):
    conn = sqlite3.connect('database.db')
    cursor = conn.cursor()

    cursor.execute("SELECT COUNT(*) FROM datapoints WHERE key=? AND value=?", (key,value))
    matching = cursor.fetchone()[0]

    cursor.execute("SELECT COUNT(*) FROM datapoints WHERE key=? ", (key,))
    total = cursor.fetchone()[0]

    conn.commit()
    conn.close()
    print("matching, total: ",matching,total)
    if(total==0):
        return 0
    return matching/total

app = Flask(__name__)

@app.route('/', methods=['POST'])
def handle_data():
    data = request.get_json()
    for kpair in data["kpairs"]:
        add_occurrence(data["uid"],kpair["key"],kpair["value"])
        print(get_rarity(kpair["key"],kpair["value"]))
    return data

if __name__ == "__main__":
    initalize_table()
    app.run()

