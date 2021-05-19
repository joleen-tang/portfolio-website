import math
import itertools
import sqlite3

con = sqlite3.connect('greenhouse.db')
cur = con.cursor()

print("combo_1")
cur.execute('SELECT COUNT(comboID) FROM combo WHERE size=1')
print(cur.fetchone()[0])

print("combo_2")
cur.execute('SELECT COUNT(comboID) FROM combo WHERE size=2')
print(cur.fetchone()[0])

print("combo_3")
cur.execute('SELECT COUNT(comboID) FROM combo WHERE size=3')
print(cur.fetchone()[0])

print("combo_4")
cur.execute('SELECT COUNT(comboID) FROM combo WHERE size=4')
print(cur.fetchone()[0])

print("combo_5")
cur.execute('SELECT COUNT(comboID) FROM combo WHERE size=5')
print(cur.fetchone()[0])

print("seed_combo test")
cur.execute('SELECT SUM(quantity) FROM seed_combo')
print(cur.fetchone()[0])

print(f"Should be: {21+231*2+1771*3+10626*4+53130*5}")