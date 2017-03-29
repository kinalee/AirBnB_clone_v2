#!/usr/bin/python3

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
    return 'C {:s}'.format(text)


@app.route('/python/')
@app.route('/python/<text>')
def python(text='is cool'):
    text = text.replace('_', ' ')
    return 'Python {:s}'.format(text)

@app.route('/number/<int:n>')
def onlyint(n):
    return '{:d} is a number'.format(n)


if __name__ == '__main__':
    app.run(host='0.0.0.0')
