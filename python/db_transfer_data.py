import sqlite3


def transfer_data(source, destination):
    # source and destination are .db files
    con = sqlite3.connect(source)
    cur = con.cursor()
    cur.execute(f'ATTACH DATABASE {destination} AS new_db')

    # Gets good combos from complete database
    cur.execute("INSERT INTO new_db.combo(comboID, size, total_rank, total_rarity)"
                "SELECT comboID, size, total_rank, total_rarity FROM combo WHERE total_rank % 12 < 3")

    # Gets combo seed compositions from complete database
    cur.execute("SELECT comboID FROM new_db.combo")
    for c_id in cur.fetchall():
        cur.execute("INSERT INTO new_db.seed_combo(comboID, seedID, quantity)"
                    f"SELECT {c_id}, seedID, quantity FROM seed_combo WHERE comboID={c_id}")


def calculate_cultivation(db_file):
    con = sqlite3.connect(db_file)
    cur = con.cursor()

    cur.execute("UPDATE combo"
                "SET no_cultivation_score = (((12 - total_rank)%12)*5)+((total_rarity/5)*4 AS INTEGER)")
    cur.execute("SELECT combo_id, no_cultivation_score FROM combo")
    combos = cur.fetchall()
    for c in combos:
        cultivation_level = 1
        while cultivation_level < 7:
            if c[1]+2*cultivation_level % 10 == 0:
                cur.execute(f"UPDATE SET cultivation_score = {c[1]+2*cultivation_level}, "
                            f"cultivation_level = {cultivation_level}")
                cultivation_level = 7


transfer_data('greenhouse.db', 'greenhouse_lite.db')
calculate_cultivation('greenhouse_lite_db_schema.py')
