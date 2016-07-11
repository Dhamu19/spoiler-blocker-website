from flask import Flask, render_template, send_from_directory, request
import os
import json

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
    data = json.loads(request.data.decode())
    testData = data['testData']
    return testData

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port, debug=True)
