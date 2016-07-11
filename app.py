from flask import Flask, render_template, send_from_directory, request
import os
from data import write_img

app = Flask(__name__)

@app.route('/')
def index():
    return render_template("index.html")

# @app.route('/img')
# def images():
#     return send_from_directory('static/img', "main.jpg")
#
# @app.route('/data', methods=['POST'])
# def py_file():
#     filedata = request.files['file']
#     return write_img(filedata)

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port, debug=True)
