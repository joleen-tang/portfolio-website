import math
import sqlite3
import flask
import os


def get_size_cultivation_level(prof_level):
    size = math.ceil(prof_level / 2)
    if prof_level == 1:
        max_cultivation_level = 1
    else:
        max_cultivation_level = size + 1
    return size, max_cultivation_level


def filter_combos(usable, cursor):
    # usable is a tuple of usable seed names
    # Returns all comboIDs that contain invalid seeds, are too large, have unwanted stats, or do not have priority stat
    s_query = 'SELECT comboID FROM seed_combo ' \
              'WHERE seedID '
    # Filter seed names
    if len(usable) == 1:
        s_query += f'!= "{usable[0]}" '
    else:
        s_query += 'NOT IN {} '.format(usable)
    s_query += 'ORDER BY comboID'
    # cursor.execute(s_query)
    # return cursor.fetchall()
    return s_query


def get_combo_info(max_cultivation_level, subquery, priority, secondary_priority, combo_limit, unwanted,
                   max_size, cursor):
    # Put rows of valid_combo_ids into one tuple
    # combo_ids = ()
    # for combo in invalid_combo_ids:
    #     combo_ids += combo
    s_query = 'SELECT combo.comboID, ' \
              f'CASE WHEN cultivation_level > ? THEN ' \
              f'zero_cultivation_score ELSE cultivation_score END AS score, ' \
              f'CASE WHEN cultivation_level > ? ' \
              f'THEN 1 ELSE cultivation_level END AS "cultivation level", ' \
              f'seed.name, seed_combo.quantity ' \
              f'FROM (combo JOIN seed_combo USING(comboID)) JOIN seed USING(seedID) ' \
              'WHERE combo.comboID NOT IN ('+subquery+') AND '
    # Filter by priority stat
    if len(priority) > 0:
        s_query += '{} > combo.size / 2 AND '.format(priority)
    # Filter out unwanted stats
    if len(unwanted) > 0:
        if len(unwanted) == 1:
            s_query += 'combo.{} == 0 AND '.format(unwanted[0])
        else:
            for stat in unwanted:
                s_query += 'combo.{} == 0 AND '.format(stat)
    # Filter by combo size
    s_query += 'combo.size <= ? '
    s_query += 'ORDER BY score DESC, '
    if len(priority) > 0:
        s_query += f'{priority} DESC, '
    if len(secondary_priority) > 0:
        s_query += f'{secondary_priority} DESC, '
    s_query += '"cultivation level", combo.comboID, seed_combo.quantity DESC, seed.name LIMIT ?'

    cursor.execute(s_query, (max_cultivation_level, max_cultivation_level, max_size, combo_limit*5))
    return cursor.fetchall()


def get_filtered_combo_ids(prof_level, priority, secondary_priority, usable, unwanted_stats, combo_limit):
    con = sqlite3.connect('greenhouse.db')
    cur = con.cursor()
    size_cult = get_size_cultivation_level(prof_level)

    # Filter out invalid combos
    invalid_combo_ids = filter_combos(usable, cur)

    # Sort valid combos and get info to be displayed
    # Output tuples (comboID, score, cultivation level, seed name, seed quantity)
    valid_combos = get_combo_info(size_cult[1], invalid_combo_ids, priority, secondary_priority, combo_limit,
                                  unwanted_stats, size_cult[0], cur)

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
    else:
        return ""
    cur.close()
    con.close()
    return combos_html


def add_seed_html(name, quantity, row_html):
    row_html += f'<td>{name}</td><td>{quantity}</td>'
    return row_html


def start_combo_row_html(score, c_level):
    return f'<tr><td>{score}</td><td>{c_level}</td>'


def end_combo_row_html(seed_count, row_html):
    # Add any required empty table cells
    for a in range(10 - seed_count * 2):
        row_html += '<td></td>'
    return row_html + '</tr>'


app = flask.Flask(__name__)
app._static_folder = os.path.abspath("templates/static/")
# csrf = CSRFProtect(app)
# app.config['SECRET_KEY'] = os.urandom(12).hex()


@app.route('/')
def index():
    return flask.render_template('fe3h_greenhouse.html')


# @app.route('/artworks')
# def artworks():
#     return flask.render_template('artworks.html')
#
#
# @app.route('/greenhouse')
# def greenhouse():
#     return flask.render_template('greenhouse.html')


@app.route('/greenhouse_query', methods=['POST'])
def greenhouse_query():
    prof_level = int(flask.request.form.get('professor_level'))
    priority = flask.request.form.get('priority')
    secondary_priority = flask.request.form.get('secondary_priority')
    usable = tuple(flask.request.form.getlist('usable'))
    u = flask.request.form.getlist('unwanted')
    if u is None:
        unwanted_stats = ()
    else:
        unwanted_stats = tuple(u)
    combo_limit = int(flask.request.form.get('combo_limit'))
    return get_filtered_combo_ids(prof_level, priority, secondary_priority, usable, unwanted_stats, combo_limit)
