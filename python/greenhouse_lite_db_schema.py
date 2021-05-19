import greenhouse_db_schema as gh
import sqlite3


def add_cultivation():
    con = sqlite3.connect('greenhouse_lite.db')
    cur = con.cursor()
    cur.execute("ALTER TABLE combo ADD COLUMN no_cultivation_score INTEGER")
    cur.execute("ALTER TABLE combo ADD COLUMN cultivation_score INTEGER")
    cur.execute("ALTER TABLE combo ADD COLUMN cultivation_level INTEGER")


gh.delete_tables('greenhouse_lite.db')
gh.set_up_seed_table('greenhouse_lite.db')
gh.set_up_combo_tables('greenhouse_lite.db')
add_cultivation()
