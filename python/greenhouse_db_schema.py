import sqlite3
import csv


def set_up_seed_table():
    con = sqlite3.connect('greenhouse.db')
    cur = con.cursor()

    cur.execute(
        'CREATE TABLE seed('
        'seedID INTEGER PRIMARY KEY, name TEXT, rank INTEGER, rarity INTEGER, stat TEXT, buyable INTEGER)')

    seeds_csv = open('FE3H_Seeds.csv')

    try:
        csv_reader = csv.reader(seeds_csv, delimiter=',')
        line_count = 0
        for row in csv_reader:
            if line_count > 0:
                cur.execute(
                    'INSERT INTO seed(name, rank, rarity, stat, buyable) '
                    f'VALUES ("{row[0]}", {row[1]}, {row[2]}, "{row[3]}", {row[4]})')
            line_count += 1
    finally:
        seeds_csv.close()
    con.commit()
    cur.close()
    con.close()


def set_up_combo_tables():
    con = sqlite3.connect('greenhouse.db')
    cur = con.cursor()

    cur.execute('DROP TABLE IF EXISTS seed_combo')
    cur.execute('DROP TABLE IF EXISTS combo')

    # Table to store combos
    cur.execute('CREATE TABLE combo('
                'comboID INTEGER PRIMARY KEY, size INTEGER, total_rank INTEGER, total_rarity INTEGER)')
    # Table to store what seeds are in what combo
    cur.execute('CREATE TABLE seed_combo('
                'comboID INTEGER, seedID INTEGER, quantity INTEGER,'
                'PRIMARY KEY(comboID, seedID),'
                'FOREIGN KEY(comboID) REFERENCES combo(comboID),'
                'FOREIGN KEY(seedID) REFERENCES seed(seedID))')
    con.commit()
    cur.close()
    con.close()


def populate_combo_tables():
    con = sqlite3.connect('greenhouse.db')
    cur = con.cursor()

    cur.execute('SELECT * FROM seed')
    single_seeds = cur.fetchall()

    for row in single_seeds:
        cur.execute('INSERT INTO combo(size, total_rank, total_rarity)'
                    f'VALUES(1, {row[2]}, {row[3]})')
        combo_id = get_max_combo_id(cur)
        cur.execute('INSERT INTO seed_combo(comboID, seedID, quantity)'
                    f'VALUES({combo_id}, {row[0]}, 1)')

    for n in range(2, 6):
        cur.execute(f'SELECT comboID, size, total_rank, total_rarity FROM combo WHERE size={n//2}')
        combo1 = cur.fetchall()

        if n % 2 == 0:
            merge_combos(combo1, combo1, cur)
        else:
            cur.execute(f'SELECT comboID, size, total_rank, total_rarity FROM combo WHERE size={n - (n // 2)}')
            combo2 = cur.fetchall()
            merge_combos(combo1, combo2, cur)

    con.commit()
    cur.close()
    con.close()


def get_max_combo_id(cur):
    cur.execute('SELECT MAX(comboID) FROM combo')
    current_combo_id = cur.fetchone()
    return current_combo_id[0]


def merge_combos(combo1, combo2, cur):
    # Each combo is tuples of (comboID, size, total_rank, total_rarity)
    for n in range(len(combo1)):    # row in combo1:
        row = combo1[n]
        for m in range(n, len(combo2)):    # other_row in combo2:
            other_row = combo2[m]
            # Insert seed combination numbers
            cur.execute('INSERT INTO combo(size, total_rank, total_rarity) '
                        f'VALUES({row[1]+other_row[1]}, {row[2] + other_row[2]}, {row[3] + other_row[3]})')
            # Get number of specific seeds in each component combo
            cur.execute(f'SELECT seedID, quantity FROM seed_combo WHERE comboID={row[0]}')
            seed_combo = cur.fetchall()
            cur.execute(f'SELECT seedID, quantity FROM seed_combo WHERE comboID={other_row[0]}')
            other_seed_combo = cur.fetchall()
            # Get current comboID
            current_combo_id = get_max_combo_id(cur)

            # Seed is tuple of (seedID, quantity)
            for seed in seed_combo:
                cur.execute('INSERT INTO seed_combo(comboID, seedID, quantity)'
                            f'VALUES({current_combo_id}, {seed[0]}, {seed[1]})')
            for seed in other_seed_combo:
                cur.execute(f'UPDATE seed_combo SET quantity = quantity + {seed[1]}'
                            f'WHERE comboID={current_combo_id} AND seedID={seed[0]}')
                cur.execute('INSERT INTO seed_combo(comboID, seedID, quantity)'
                            f'SELECT {current_combo_id}, {seed[0]}, {seed[1]}'
                            f'WHERE (SELECT changes() = 0)')



def delete_tables():
    con = sqlite3.connect('greenhouse.db')
    cur = con.cursor()

    cur.execute('DROP TABLE IF EXISTS seed_combo')
    cur.execute('DROP TABLE IF EXISTS seed')
    cur.execute('DROP TABLE IF EXISTS combo')

    con.commit()
    cur.close()
    con.close()


delete_tables()
set_up_seed_table()
set_up_combo_tables()
populate_combo_tables()