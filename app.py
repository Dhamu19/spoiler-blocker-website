from flask import Flask, render_template, request
from datetime import datetime
import json
import os
from helper import full_text_search, full_title_search, set_cookie
from db_connector import db_connection, db_cursor
import config
from flask.ext.compress import Compress

app = Flask(__name__)
Compress(app)


@app.route('/')
def index():
    return render_template("index.html")


@app.route('/getLists', methods=['POST'])
def getLists():
    cookie = json.loads(request.cookies.get('ratings', "{}"))
    data = json.loads(request.data.decode())

    conn = db_connection()
    cur = db_cursor(conn)

    result, count = full_text_search(data['query'], data['pageNum'], cur)

    for i, json_obj in enumerate(result):
        if str(json_obj['id']) in cookie:
            result[i]['user_rating_from_cookie'] = cookie[str(json_obj['id'])]

    conn.close()
    return json.dumps({'result': result, 'count': count})


@app.route('/getTitles', methods=['POST'])
def getTitles():
    conn = db_connection()
    cur = db_cursor(conn)

    data = json.loads(request.data.decode())
    results = full_title_search(data['query'], cur)

    conn.close()

    if len(results) == 0:
        return json.dumps(['No results found'])
    else:
        return json.dumps(results)


@app.route('/postsPerPage', methods=['GET'])
def postsPerPage():
    return str(config.ROWS_PER_PAGE)


@app.route('/createList', methods=['POST'])
def createList():
    conn = db_connection()
    cur = db_cursor(conn)

    data = json.loads(request.data.decode())
    cur.execute(
        'INSERT INTO pending_lists (title, tags, date_added, email) VALUES (%s, %s, %s, %s);',
        (data['title'], data['tags'], datetime.now(), data['email'])
    )
    conn.commit()

    conn.close()

    return json.dumps({'Status': 'Success'})


@app.route('/rateList', methods=['POST'])
def rateList():
    conn = db_connection()
    cur = db_cursor(conn)

    data = json.loads(request.data.decode())
    cur.execute(
        'SELECT rating, num_ratings FROM spoiler_lists WHERE id=%s',
        (data['id'], )
    )
    ratingDict = dict(cur.fetchone())

    return_val = set_cookie(str(data['id']), data['rating'], ratingDict, conn, cur)

    conn.close()
    return return_val


@app.route('/downloadList', methods=['GET'])
def downloadList():
    conn = db_connection()
    cur = db_cursor(conn)

    listID = request.args.get('id', '')
    cur.execute('SELECT title, tags, num_downloads FROM spoiler_lists WHERE id=%s', (listID,))
    spoilerList = cur.fetchone()

    if spoilerList:
        cur.execute('UPDATE spoiler_lists SET num_downloads=%s WHERE id=%s', (spoilerList['num_downloads'] + 1, listID))
        conn.commit()
        conn.close()
        return json.dumps({'list': dict(spoilerList), 'Status': 'Success'})
    else:
        conn.close()
        return json.dumps({'Status': 'Does Not Exist'})

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port, debug=True)
