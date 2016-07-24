from flask import Flask, render_template, request, jsonify
from datetime import date, datetime
import json
from helper import full_text_search, cur, conn, os

app = Flask(__name__)

@app.route('/')
def index():
    return render_template("index.html")

@app.route('/getLists', methods=['POST'])
def getLists():
    data = json.loads(request.data.decode())
    return json.dumps(full_text_search(data['query']))

@app.route('/createList', methods=['POST'])
def createList():
    data = json.loads(request.data.decode())
    cur.execute(
        'INSERT INTO pending_lists (title, tags, date_added, email) VALUES (%s, %s, %s, %s);',
        (data['title'], data['tags'], datetime.now(), data['email'])
    )
    conn.commit()
    return json.dumps({'Status': 'Success'})

@app.route('/rateList', methods=['POST'])
def rateList():
    data = json.loads(request.data.decode())
    cur.execute('SELECT rating, num_ratings FROM block_lists WHERE id=%s', (data['id'], ))
    ratingDict = dict(cur.fetchone())

    response = set_cookie({'newRating': newRating, 'Status': 'Success'}, str(data['id']), ratingDict)
    return response

def set_cookie(newRating, list_ID, ratingDict):
    is_new_rating = True

    if (request.cookies.get('ratings')) is None:
        is_new_rating = True
    else:
        cookie = json.loads(request.cookies.get('ratings'))
        if list_ID in cookie:
            is_new_rating = False
        else:
            is_new_rating = True

    if is_new_rating:
        newNumRatings = ratingDict['num_ratings'] + 1
        newRating = (ratingDict['rating'] * ratingDict['num_ratings'] + data['rating']) / (newNumRatings)
        cur.execute('UPDATE block_lists SET rating=%s, num_ratings=%s WHERE id=%s', (newRating, newNumRatings, data['id']))
        conn.commit()
        

    resp.set_cookie('ratings', json.dumps({list_ID: 0}))

    cookie[list_ID] = 0
    resp.set_cookie('ratings', json.dumps(cookie))
    return resp


@app.route('/downloadList', methods=['GET'])
def downloadList():
    listID = request.args.get('id', '')
    cur.execute('SELECT title, tags, num_downloads FROM block_lists WHERE id=%s', (listID,))
    spoilerList = cur.fetchone()
    if spoilerList:
        cur.execute('UPDATE block_lists SET num_downloads=%s WHERE id=%s', (spoilerList['num_downloads'] + 1, listID))
        conn.commit()
        return json.dumps({'list': dict(spoilerList), 'Status': 'Success'})
    else:
        return json.dumps({'Status': 'Does Not Exist'})

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port, debug=True)
    cur.close()
    conn.close()
