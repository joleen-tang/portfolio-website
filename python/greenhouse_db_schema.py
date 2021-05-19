import sqlite3
import csv
import itertools


def set_up_seed_table(db_file):
    con = sqlite3.connect(db_file)
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


def set_up_combo_tables(db_file):
    con = sqlite3.connect(db_file)
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
    seeds = cur.fetchall()

    temp = [n for n in range(21)]

    for n in range(1, 6):
        seed_ids = list(itertools.combinations_with_replacement(temp, n))
        create_combos(seeds, seed_ids, cur)

    con.commit()
    cur.close()
    con.close()


def get_max_combo_id(cur):
    cur.execute('SELECT MAX(comboID) FROM combo')
    current_combo_id = cur.fetchone()
    return current_combo_id[0]


def create_combos(seeds, seed_ids, cur):
    # SeedIDs is a tuple of seed IDs,
    # seeds is the tuple of tuples of all seeds pulled from seed table (seedID, name, rank, rarity, stat, buyable)
    for combination in seed_ids:
        size = 0
        rank = 0
        rarity = 0
        for s_id in combination:
            size += 1
            rank += seeds[s_id][2]
            rarity += seeds[s_id][3]
        # Insert seed combination numbers
        cur.execute('INSERT INTO combo(size, total_rank, total_rarity) '
                    f'VALUES({size}, {rank}, {rarity})')
        # Get current comboID
        current_combo_id = get_max_combo_id(cur)
        for s_id in combination:
            cur.execute(f'UPDATE seed_combo '
                        f'SET quantity = quantity + 1 WHERE comboID={current_combo_id} AND seedID={s_id}')
            cur.execute('INSERT INTO seed_combo(comboID, seedID, quantity)'
                        f'SELECT {current_combo_id}, {s_id}, 1 WHERE (SELECT changes() = 0)')


def delete_tables(db_file):
    con = sqlite3.connect(db_file)
    cur = con.cursor()

    cur.execute('DROP TABLE IF EXISTS seed_combo')
    cur.execute('DROP TABLE IF EXISTS seed')
    cur.execute('DROP TABLE IF EXISTS combo')

    con.commit()
    cur.close()
    con.close()


delete_tables('greenhouse.db')
set_up_seed_table('greenhouse.db')
set_up_combo_tables('greenhouse.db')
populate_combo_tables()
