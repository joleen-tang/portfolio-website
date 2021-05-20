import sqlite3
import math

con = sqlite3.connect('greenhouse.db')
con2 = sqlite3.connect('greenhouse_lite.db')
cur = con.cursor()
cur2 = con2.cursor()

print('Best 5 seed-combos in greenhouse_lite.db')
cur2.execute('SELECT combo.comboID, combo.zero_cultivation_score, seed.name, seed_combo.quantity FROM (combo JOIN seed_combo ON combo.comboID=seed_combo.comboID) JOIN seed USING (seedID) WHERE combo.zero_cultivation_score>80 ORDER BY zero_cultivation_score')
count=0
for row in cur2.fetchall():
   print(row)
   count+=1
print(count)
# print("\n\nGREENHOUSE_LITE")
# cur2.execute('SELECT combo.comboID, seed.name, seed_combo.quantity FROM (combo JOIN seed_combo ON combo.comboID=seed_combo.comboID) JOIN seed USING (seedID) WHERE total_rarity>23 AND ORDER BY total_rarity')
# count=0
# for row in cur2.fetchall():
#    print(row)
#    count+=1
# print(count)
# #
# cur2.execute('SELECT combo.zero_cultivation_score, combo.cultivation_score, combo.cultivation_level, seed.name, seed_combo.quantity FROM (combo JOIN seed_combo ON combo.comboID=seed_combo.comboID) JOIN seed USING (seedID) WHERE combo.comboID=52790')
# for row in cur2.fetchall():
#    print(row)