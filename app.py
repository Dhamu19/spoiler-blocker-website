from flask import Flask, render_template, request
from datetime import date, datetime
import json
from helper import fullTextSearch, cur, conn, os

app = Flask(__name__)

@app.route('/')
def index():
    return render_template("index.html")

@app.route('/getLists', methods=['POST'])
def getLists():
    data = json.loads(request.data.decode())
    return json.dumps(fullTextSearch(data['query']))

@app.route('/createList', methods=['POST'])
def createList():
    data = json.loads(request.data.decode())
    cur.execute(
        'INSERT INTO pending_lists (title, tags, date_added, email) VALUES (%s, %s, %s, %s);',
        (data['title'], data['tags'], datetime.now(), data['email'])
    )
    conn.commit()
    return json.dumps({'Status': 'Success'})

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port, debug=True)
    cur.close()
    conn.close()
