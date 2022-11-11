#!/usr/bin/python3
"""
    starts a Flask web application
"""

from flask import Flask, render_template
from models import storage
from models.state import State

app = Flask(__name__)


@app.route('/cities_by_states', strict_slashes=False)
def city_by_state():
    """
        displays a HTML page containing a list of states and cities
    """
    states = sorted(list(storage.all(State).values()), key=lambda x: x.name)
    return render_template('8-cities_by_states.html', states=states)


@app.teardown_appcontext
def teardown_db(exception):
    """
        removes the current SQLAlchemy session after each request
    """
    storage.close()


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
