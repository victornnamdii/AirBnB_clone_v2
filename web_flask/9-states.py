#!/usr/bin/python3
"""
    starts a Flask web application
"""

from flask import Flask, render_template
from models import storage
from models.state import State

app = Flask(__name__)


@app.route('/states', strict_slashes=False)
@app.route('/states/<id>', strict_slashes=False)
def get_state(id=None):
    """
        displays a HTML page containing a list of states and cities
    """
    states = storage.all(State)
    if id is not None:
        id = 'State.' + id
    return render_template('9-states.html', id=id, states=states)


@app.teardown_appcontext
def teardown_db(exception):
    """
        removes the current SQLAlchemy session after each request
    """
    storage.close()


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
