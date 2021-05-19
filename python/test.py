import math
import itertools
import sqlite3

con = sqlite3.connect('greenhouse.db')
con2 = sqlite3.connect('greenhouse_lite.db')
cur = con.cursor()
cur2 = con2.cursor()

print('Best 5 seed-combos in greenhouse_lite.db')
cur2.execute('SELECT combo.comboID, combo.total_rank, seed.seedID, seed.name, seed_combo.quantity FROM (combo JOIN seed_combo ON combo.comboID=seed_combo.comboID) JOIN seed USING (seedID) WHERE (combo.total_rank % 12)=0 AND combo.size=5')
for row in cur2.fetchall():
    print(row)
