import sqlite3
import flask
import math


def get_size_cultivation_level(prof_level):
    size = math.ceil(prof_level / 2)
    if prof_level == 1:
        max_cultivation_level = 1
    else:
        max_cultivation_level = size + 1
    return size, max_cultivation_level


def filter_size_stats(max_size, priority, cursor):
    # Returns all comboIDs that prioritize the given stat and are of a valid size
    s_query = f'SELECT comboID FROM combo WHERE '
    if len(priority) > 0:
        s_query += '{} > size / 2 AND size <= ? ORDER BY comboID'.format(priority)
        cursor.execute(s_query, (max_size,))
    else:
        s_query += f'size <= ? ORDER BY comboID'
        cursor.execute(s_query, (max_size,))
    return cursor.fetchall()


def filter_seeds(unusable, cursor):
    # unusable is a tuple of unusable seedIDs)
    # Returns all comboIDs that contain invalid seeds
    if unusable is not None:
        s_query = 'SELECT combo.comboID FROM combo JOIN seed_combo USING(comboID) WHERE seed_combo.seedID '
        if len(unusable) == 1:
            s_query += f'= {unusable[0]} '
        else:
            s_query += 'IN {} '.format(unusable)
        s_query += 'ORDER BY combo.comboID'
        cursor.execute(s_query)
        return cursor.fetchall()
    else:
        return ()


def get_combo_info(max_cultivation_level, valid_combo_ids, priority, secondary_priority, cursor):
    # Put rows of valid_combo_ids into one tuple
    combo_ids = ()
    for combo in valid_combo_ids:
        combo_ids += combo

    s_query = 'SELECT combo.comboID, ' \
              f'CASE WHEN cultivation_level > ? THEN ' \
              f'zero_cultivation_score ELSE cultivation_score END AS score, ' \
              f'CASE WHEN cultivation_level > ? ' \
              f'THEN 1 ELSE cultivation_level END AS "cultivation level", ' \
              f'seed.name, seed_combo.quantity ' \
              f'FROM (combo JOIN seed_combo USING(comboID)) JOIN seed USING(seedID) ' \
              'WHERE combo.comboID IN {} '.format(combo_ids)
    s_query += f'ORDER BY score DESC, {priority} DESC, {secondary_priority} DESC, "cultivation level", ' \
               f'size, combo.comboID'

    cursor.execute(s_query, (max_cultivation_level, max_cultivation_level))
    return cursor.fetchall()


app = flask.Flask(__name__)


@app.route('/')
def get_filtered_combo_ids(prof_level, priority, secondary_priority, unusable, combo_limit):
    con = sqlite3.connect('greenhouse_lite.db')
    cur = con.cursor()
    size_cult = get_size_cultivation_level(prof_level)

    # Filter out invalid combos
    size_priority_filtered = filter_size_stats(size_cult[0], priority, cur)
    seed_filtered = filter_seeds(unusable, cur)
    valid_combo_ids = tuple(set(size_priority_filtered).difference(set(seed_filtered)))

    # Sort valid combos and get info to be displayed
    # Output tuples (comboID, score, cultivation level, seed name, seed quantity)
    valid_combos = get_combo_info(size_cult[1], valid_combo_ids, priority, secondary_priority, cur)

    # Format valid combos into HTML table rows
    combos_html = ''
    if len(valid_combos) > 0:
        current_id = valid_combos[0][0]
        row_html = start_combo_row_html(valid_combos[0][1], valid_combos[0][2])
        combo_seed_count = 0
        combo_count = 0
        for row in valid_combos:
            if row[0] != current_id:
                # Check if max combos has been reached
                combo_count += 1
                if combo_count == combo_limit:
                    break

                # End previous row
                row_html = end_combo_row_html(combo_seed_count, row_html)
                combos_html += row_html

                # Start next row
                combo_seed_count = 0
                current_id = row[0]
                row_html = start_combo_row_html(row[1], row[2])
            row_html = add_seed_html(row[3], row[4], row_html)
            combo_seed_count += 1
        row_html = end_combo_row_html(combo_seed_count, row_html)
        combos_html += row_html

    cur.close()
    con.close()
    return combos_html


def add_seed_html(name, quantity, row_html):
    row_html += f'\t<td>{name}</td><td>{quantity}</td>\n'
    return row_html


def start_combo_row_html(score, c_level):
    return f'<tr>\n\t<td>{score}</td>\n\t<td>{c_level}</td>\n'


def end_combo_row_html(seed_count, row_html):
    # Add any required empty table cells
    for a in range(10 - seed_count * 2):
        row_html += '\t<td></td>\n'
    return row_html + '</tr>\n'


print(get_filtered_combo_ids(9, 'speed', 'luck', (21,), 50))
