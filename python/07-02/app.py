# -*- coding: utf-8 -*-
import flask

app = flask.Flask(__name__)


#
@app.route('/')
def index():
    return "Hello, World!"


if __name__ == '__main__':
    app.run(debug=False, host='0.0.0.0', port=5000)
