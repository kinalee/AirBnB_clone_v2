#!/usr/bin/python3

import os
from flask import Flask, render_template

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
    return 'C {:s}'.format(text)

@app.route('/python/')
@app.route('/python/<text>')
def python(text='is cool'):
    text = text.replace('_', ' ')
    return 'Python {:s}'.format(text)

@app.route('/number/<n>')
def onlyint(n):
    if int(n):
        return '{:d} is a number'.format(int(n))

@app.route('/number_template/<n>')
def onlyinttemp(n):
    if int(n):
        return render_template("5-number.html", n = int(n))

@app.route('/number_odd_or_even/<n>')
def evenorodd(n):
    if int(n):
        if int(n) % 2 == 0:
            return render_template("6-number_odd_or_even.html", n = int(n),
                                   evenodd="even")
        else:
            return render_template("6-number_odd_or_even.html", n = int(n),
                                   evenodd="odd")


if __name__ == '__main__':
    app.run(host='0.0.0.0')
