#!/usr/bin/python3
"""
    Starts a Flask web application
"""

from flask import Flask
app = Flask(__name__)


@app.route('/', strict_slashes=False)
def index():
    """
        returns Hello HBNB!
    """
    return 'Hello HBNB!'


@app.route('/hbnb', strict_slashes=False)
def hbnb():
    """
        returns HBNB
    """
    return 'HBNB'


@app.route('/c/<text>', strict_slashes=False)
def croute(text):
    """
        displays C followed by the text
    """
    return 'C ' + text.replace('_', ' ')


@app.route('/python', strict_slashes=False)
@app.route('/python/<text>', strict_slashes=False)
def pyroute(text='is cool'):
    """
        displays Python followed by the text
    """
    return 'Python ' + text.replace('_', ' ')


@app.route('/number/<int:n>', strict_slashes=False)
def number(n):
    """
        displays n is anumber if n is an integer
    """
    return '{:d} is a number'.format(n)


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
