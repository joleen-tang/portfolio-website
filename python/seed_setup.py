import sqlite3
import csv


def setUpSeedTable():
    con = sqlite3.connect('greenhouse.db')

    cur = con.cursor()
    cur.execute('DROP TABLE seed')
    cur.execute(
        'CREATE TABLE IF NOT EXISTS seed('
        'seedID INTEGER PRIMARY KEY,name TEXT, rank INTEGER, rarity INTEGER, stat TEXT, buyable INTEGER)')

    seedsCSV = open('FE3H_Seeds.csv')

    try:
        csv_reader = csv.reader(seedsCSV, delimiter=',')
        line_count = 0
        for row in csv_reader:
            if line_count > 0:
                cur.execute(
                    f'INSERT INTO seed(name, rank, rarity, stat, buyable) '
                    f'VALUES ("{row[0]}", {row[1]}, {row[2]}, "{row[3]}", {row[4]})')
            line_count += 1
    finally:
        seedsCSV.close()

    cur.close()

