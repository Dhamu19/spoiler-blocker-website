from flask import Flask, render_template, request
from datetime import date, datetime
# import flask.ext.login as flask_login
import json
from helper import fullTextSearch, cur, conn

app = Flask(__name__)

class DateEncoder(json.JSONEncoder):

    def default(self, obj):
        if isinstance(obj, date):
            return str(obj)
        return json.JSONEncoder.default(self, obj)

# # Login Manager
# app.secret_key = 'super secret string'  # Change this!
# login_manager = flask_login.LoginManager()
# login_manager.init_app(app)
#
# class User(flask_login.UserMixin):
#     def is_active(self):
#         """True, as all users are active."""
#         return True
#
#     def get_id(self):
#         """Return the email address to satisfy Flask-Login's requirements."""
#         return self.email
#
#     def is_authenticated(self):
#         """Return True if the user is authenticated."""
#         return self.authenticated
#
#     def is_anonymous(self):
#         """False, as anonymous users aren't supported."""
#         return False
#
# @login_manager.user_loader
# def user_loader(username):
#     if not username_exists(username):
#         return
#
#     user = User()
#     user.id = username
#     return user
#
# def username_exists(username):
#     cur.execute("select exists(select 1 from users where username=%s);", (username,))
#     return cur.fetchone()[0]

@app.route('/')
def index():
    return render_template("index.html")

@app.route('/lists')
def lists():
    return render_template("lists.html")

@app.route('/getLists', methods=['POST'])
def getLists():
    data = json.loads(request.data.decode())
    numLists = data['numLists']
    cur.execute("SELECT * FROM block_lists;")
    return json.dumps(map(dict, cur.fetchall()), cls=DateEncoder)

@app.route('/listForm')
def listForm():
    return render_template("create_list.html")

@app.route('/createList', methods=['POST'])
def createList():
    data = json.loads(request.data.decode())
    cur.execute(
        'INSERT INTO pending_lists (title, tags, date_added, email) VALUES (%s, %s, %s, %s);',
        (data['title'], data['tags'], datetime.now(), data['email'])
    )
    conn.commit()
    return json.dumps({'Status': 'Success'})

@app.route('/searchLists', methods=['POST'])
def searchLists():
    data = json.loads(request.data.decode())
    return json.dumps(fullTextSearch(data['query']))

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port, debug=True)
    cur.close()
    conn.close()
