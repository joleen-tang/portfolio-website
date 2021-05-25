import sqlite3
import math


def transfer_data(source, destination):
    # source and destination are .db files
    con = sqlite3.connect(source)
    cur = con.cursor()
    cur.execute(f'ATTACH DATABASE "{destination}" AS new_db')

    # Gets good combos from complete database
    cur.execute('INSERT INTO new_db.combo (comboID, size, total_rank, total_rarity)'
                'SELECT comboID, size, total_rank, total_rarity FROM combo WHERE total_rank % 12 < 3 '
                'OR size=1')

    # Gets combo seed compositions from complete database
    cur.execute("SELECT comboID FROM new_db.combo")
    for c_id in cur.fetchall():
        cur.execute('INSERT INTO new_db.seed_combo (comboID, seedID, quantity)'
                    f'SELECT comboID, seedID, quantity FROM seed_combo WHERE comboID={c_id[0]}')
    con.commit()
    cur.close()
    con.close()


def calculate_cultivation(db_file):
    con = sqlite3.connect(db_file)
    cur = con.cursor()

    cur.execute('SELECT comboID, total_rank, total_rarity FROM combo')
    combos = cur.fetchall()

    for c in combos:
        zero_update_query = 'UPDATE combo set zero_cultivation_score = ' + str(get_effective_score(get_score(c, 1))) + \
                            ' WHERE comboID = '+str(c[0])
        cur.execute(zero_update_query)
        cultivation_level = 2
        while cultivation_level < 7:
            score = get_score(c, cultivation_level)
            if score % 10 == 2 or score % 10 == 1:
                update_query = 'UPDATE combo SET cultivation_score = '+str(get_effective_score(score)) + \
                               ', cultivation_level = ' + str(cultivation_level)+' WHERE comboID = '+str(c[0])
                cur.execute(update_query)
                break
            cultivation_level += 1
    con.commit()
    cur.close()
    con.close()


def get_score(combo, cultivation_level):
    # combo is a tuple (comboID, total_rank, total_rarity)
    a = (12 - (combo[1] % 12)) * 5
    b = math.floor((combo[2] / 5) * 4)
    c = (cultivation_level+4) * 2
    return a + b + c


def get_effective_score(score):
    return score // 10


def populate_combo_stats():
    con = sqlite3.connect('greenhouse_lite.db')
    cur = con.cursor()

    cur.execute('SELECT seed_combo.comboID, seed.stat, seed_combo.quantity FROM seed_combo JOIN seed USING (seedID)')
    for row in cur.fetchall():
        query_string = 'UPDATE combo SET '+row[1].lower()+' = '+row[1].lower()+' + '+str(row[2])\
                       + ' WHERE comboID = '+str(row[0])
        cur.execute(query_string)

    con.commit()
    cur.close()
    con.close()


transfer_data('greenhouse.db', 'greenhouse_lite.db')
calculate_cultivation('greenhouse_lite.db')
populate_combo_stats()
