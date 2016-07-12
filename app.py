from flask import Flask, render_template, send_from_directory, request
import os
import json
import psycopg2
import psycopg2.extras
import urlparse

urlparse.uses_netloc.append("postgres")
url = urlparse.urlparse(os.environ["DATABASE_URL"])

conn = psycopg2.connect(
    database=url.path[1:],
    user=url.username,
    password=url.password,
    host=url.hostname,
    port=url.port
)
cur = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)

app = Flask(__name__)

@app.route('/')
def index():
    return render_template("index.html")

# @app.route('/img')
# def images():
#     return send_from_directory('static/img', "main.jpg")
#
@app.route('/testRoute', methods=['POST'])
def test():
    # data = json.loads(request.data.decode())
    # testData = data['testData']
    # return testData
    cur.execute("SELECT * FROM test_table;")
    return cur.fetchone()['text']

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port, debug=True)
    cur.close()
    conn.close()
