import sqlite3
import math

def setUpComboTables():
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
    cur.close()
    con.close()

def populateComboTable():
    con = sqlite3.connect('greenhouse.db')
    cur = con.cursor()

    cur.execute('SELECT * FROM seed')
    single_seeds = cur.fetchall()

    for row in single_seeds:
        # score = ((12-(row[2] % 12))*5+math.floor((row[3]/5)*4))
        cur.execute('INSERT INTO combo(size, total_rank, total_rarity)'
                    f'VALUES(1, {row[2]}, {row[3]})')
        cur.execute("SELECT MAX(comboID) FROM combo")
        combo_id = cur.fetchone()
        cur.execute('INSERT INTO seed_combo(comboID, seedID, quantity)'
                    f'VALUES({combo_id[0]}, {row[0]}, 1)')

    for n in range(1, 5):
        cur.execute(f'SELECT comboID, total_rank, total_rarity FROM combo WHERE size={n}')
        n_seeds_combo = cur.fetchall()

        for row in n_seeds_combo:
            for single_row in single_seeds:
                # Insert seed combination numbers
                cur.execute('INSERT INTO combo(size, total_rank, total_rarity) '
                            f'VALUES({n+1}, {row[1]+single_row[2]}, {row[2]+single_row[3]})')

                # Get number of specific seeds in non-singular combo component
                cur.execute(f'SELECT seedID, quantity FROM seed_combo WHERE comboID={row[0]}')
                component_seed_combo = cur.fetchall()
                # Get current comboID
                cur.execute('SELECT MAX(comboID) FROM combo')
                current_combo_id = cur.fetchone()
                duplicate_seed = False

                for component_row in component_seed_combo:
                    if component_row[0] == single_row[0]:
                        cur.execute('INSERT INTO seed_combo(comboID, seedID, quantity)'
                                    f'VALUES({current_combo_id[0]}, {component_row[0]}, {component_row[1]+1})')
                        duplicate_seed = True
                    else:
                        cur.execute('INSERT INTO seed_combo(comboID, seedID, quantity)'
                                    f'VALUES({current_combo_id[0]}, {component_row[0]}, {component_row[1]})')
                if not duplicate_seed:
                    cur.execute('INSERT INTO seed_combo(comboID, seedID, quantity)'
                                f'VALUES({current_combo_id[0]}, {single_row[0]}, 1)')
    cur.close()
    con.close()


setUpComboTables()
populateComboTable()
