import sqlite3
import csv
import itertools
import math


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
                'comboID INTEGER PRIMARY KEY, '
                'size INTEGER, '
                'total_rank INTEGER, '
                'total_rarity INTEGER, '
                'zero_cultivation_score INTEGER, '
                'cultivation_score INTEGER, '
                'cultivation_level INTEGER, '
                'hp INTEGER DEFAULT(0), '
                'strength INTEGER DEFAULT(0), '
                'magic INTEGER DEFAULT(0), '
                'dexterity INTEGER DEFAULT(0), '
                'speed INTEGER DEFAULT(0), '
                'luck INTEGER DEFAULT(0), '
                'defence INTEGER DEFAULT(0), '
                'resistance INTEGER DEFAULT(0), '
                'charm INTEGER DEFAULT(0))')
    # Table to store what seeds are in what combo
    cur.execute('CREATE TABLE seed_combo('
                'comboID INTEGER, seedID INTEGER, quantity INTEGER,'
                'PRIMARY KEY(comboID, seedID),'
                'FOREIGN KEY(comboID) REFERENCES combo(comboID),'
                'FOREIGN KEY(seedID) REFERENCES seed(seedID))')
    con.commit()
    cur.close()
    con.close()


def populate_combo_tables(db_file):
    con = sqlite3.connect(db_file)
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
                        f'SET quantity = quantity + 1 WHERE comboID={current_combo_id} AND seedID={s_id+1}')
            cur.execute('INSERT INTO seed_combo(comboID, seedID, quantity)'
                        f'SELECT {current_combo_id}, {s_id+1}, 1 WHERE (SELECT changes() = 0)')


def delete_tables(db_file):
    con = sqlite3.connect(db_file)
    cur = con.cursor()

    cur.execute('DROP TABLE IF EXISTS seed_combo')
    cur.execute('DROP TABLE IF EXISTS seed')
    cur.execute('DROP TABLE IF EXISTS combo')

    con.commit()
    cur.close()
    con.close()


def create_indexes(db_file):
    con = sqlite3.connect(db_file)
    cur = con.cursor()

    cur.execute("CREATE INDEX IF NOT EXISTS idx_combo ON combo (cultivation_score, size)")
    cur.execute("CREATE INDEX IF NOT EXISTS idx_seed_combo ON seed_combo (quantity)")
    cur.execute("CREATE INDEX IF NOT EXISTS idx_seed ON seed (name)")

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


def populate_combo_stats(db_file):
    con = sqlite3.connect(db_file)
    cur = con.cursor()

    cur.execute('SELECT seed_combo.comboID, seed.stat, seed_combo.quantity FROM seed_combo JOIN seed USING (seedID)')
    for row in cur.fetchall():
        query_string = 'UPDATE combo SET '+row[1].lower()+' = '+row[1].lower()+' + '+str(row[2])\
                       + ' WHERE comboID = '+str(row[0])
        cur.execute(query_string)

    con.commit()
    cur.close()
    con.close()


delete_tables('../greenhouse.db')
set_up_seed_table('../greenhouse.db')
set_up_combo_tables('../greenhouse.db')
populate_combo_tables('../greenhouse.db')
create_indexes('../greenhouse.db')
calculate_cultivation('../greenhouse.db')
populate_combo_stats('../greenhouse.db')
