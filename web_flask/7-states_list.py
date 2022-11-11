#!/usr/bin/python3
"""
    starts a Flask web application
"""

from flask import Flask, render_template
from models import storage
from models.state import State

app = Flask(__name__)


@app.route('/states_list', strict_slashes=False)
def state_city():
    """
        displays a HTML page containing a list of states
    """
    states = sorted(list(storage.all(State).values()), key=lambda x: x.name)
    print(str(states) + 'COOO')
    return render_template('7-states_list.html', states=states)


@app.teardown_appcontext
def teardown_db(exception):
    """
        removes the current SQLAlchemy session after each request
    """
    storage.close()


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
