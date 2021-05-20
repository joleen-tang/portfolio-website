import sqlite3


def get_size_cultivation_level(prof_level):
    if prof_level < 2:
        size = 1
        if prof_level == 1:
            max_cultivation_level = 2
        else:
            max_cultivation_level = 1
    elif 1 < prof_level < 4:
        size = 2
        max_cultivation_level = 3
    elif 3 < prof_level < 6:
        size = 3
        max_cultivation_level = 4
    elif 5 < prof_level < 8:
        size = 4
        max_cultivation_level = 5
    else:
        size = 5
        max_cultivation_level = 6
    return size, max_cultivation_level


def filter_size_stats(max_size, priority, cursor):
    s_query = f'SELECT comboID ' \
              f'FROM combo ' \
              f'WHERE {priority} > size / 2 AND size <= {max_size} ' \
              f'ORDER BY comboID'
    cursor.execute(s_query)
    # return list of tuples (comboID)
    return cur.fetchall()


def filter_seeds(unusable, combos, cursor):
    # unusable is a tuple of unusable seedIDs)
    # combos is a list of combination tuples (comboID)
    if unusable is not None:
        s_query = 'SELECT combo.comboID FROM combo JOIN seed_combo USING(comboID) ' \
                  f'WHERE seed_combo.seedID '
        if len(unusable) > 1:
            s_query += f'IN {unusable} '
        else:
            s_query += f'= {unusable[0]} '
        s_query += 'ORDER BY combo.comboID'
        cursor.execute(s_query)
        combos2 = set(cursor.fetchall())
        return tuple(set(combos)-combos2)
    else:
        return combos


def sort_cultivation_level(max_cultivation_level, combos, cursor):
    # combos is list of current potential combos
    s_query = 'SELECT combo.comboID, ' \
            f'CASE WHEN cultivation_level > {max_cultivation_level} THEN ' \
            f'zero_cultivation_score ELSE cultivation_score END AS score, ' \
            f'CASE WHEN cultivation_level > {max_cultivation_level} ' \
            f'THEN 1 ELSE cultivation_level END AS "cultivation level", ' \
            f'combo.size, seed.name, seed_combo.quantity'


con = sqlite3.connect('greenhouse_lite.db')
cur = con.cursor()

results = filter_size_stats(8, 'speed', cur)
results = filter_seeds((21,), results, cur)

count = 0
for row in results:
    print(row)
    count += 1
print(count)
