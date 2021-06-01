import greenhouse_db_schema as gh
import sqlite3


def add_cultivation():
    con = sqlite3.connect('greenhouse_lite.db')
    cur = con.cursor()
    cur.execute("ALTER TABLE combo ADD COLUMN zero_cultivation_score INTEGER")
    cur.execute("ALTER TABLE combo ADD COLUMN cultivation_score INTEGER")
    cur.execute("ALTER TABLE combo ADD COLUMN cultivation_level INTEGER")


def add_stats():
    con = sqlite3.connect('greenhouse_lite.db')
    cur = con.cursor()

    cur.execute("ALTER TABLE combo ADD COLUMN hp INTEGER DEFAULT(0)")
    cur.execute("ALTER TABLE combo ADD COLUMN strength INTEGER DEFAULT(0)")
    cur.execute("ALTER TABLE combo ADD COLUMN magic INTEGER DEFAULT(0)")
    cur.execute("ALTER TABLE combo ADD COLUMN dexterity INTEGER DEFAULT(0)")
    cur.execute("ALTER TABLE combo ADD COLUMN speed INTEGER DEFAULT(0)")
    cur.execute("ALTER TABLE combo ADD COLUMN luck INTEGER DEFAULT(0)")
    cur.execute("ALTER TABLE combo ADD COLUMN defence INTEGER DEFAULT(0)")
    cur.execute("ALTER TABLE combo ADD COLUMN resistance INTEGER DEFAULT(0)")
    cur.execute("ALTER TABLE combo ADD COLUMN charm INTEGER DEFAULT(0)")

    con.commit()
    cur.close()
    con.close()


def create_indexes():
    con = sqlite3.connect('greenhouse_lite.db')
    cur = con.cursor()

    cur.execute("CREATE INDEX IF NOT EXISTS idx_combo ON combo (cultivation_score, size)")
    cur.execute("CREATE INDEX IF NOT EXISTS idx_seed_combo ON seed_combo (quantity)")
    cur.execute("CREATE INDEX IF NOT EXISTS idx_seed ON seed (name)")

    con.commit()
    cur.close()
    con.close()


gh.delete_tables('greenhouse_lite.db')
gh.set_up_seed_table('greenhouse_lite.db')
gh.set_up_combo_tables('greenhouse_lite.db')
add_cultivation()
add_stats()
create_indexes()
