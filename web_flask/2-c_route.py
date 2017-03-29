#!/usr/bin/python3

import os
from flask import Flask

app = Flask(__name__)


@app.route('/')
def index():
    return 'Hello HBNB!'


@app.route('/hbnb')
def return_hbnb():
    return 'HBNB'


@app.route('/c/<text>')
def cisfun(text):
    text = text.replace('_', ' ')
    return 'c {:s}'.format(text)

if __name__ == '__main__':
    app.run(host='0.0.0.0')
