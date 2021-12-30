import sqlite3
import click
from flask import current_app, g
from flask.cli import with_appcontext
'''
Connect to the DB: In web app, connection is tied to the request. It is created at some point when handling a request and closed before the response is sent.
'''

def get_db():
    '''
    g: Special object which is unique for each request.
        => Store data and accesses by multiple functions during request.
        => connection is stored and reused if get_db() again called in same request
    current_app: current_app is used to handle request when app has been created
    '''
    if 'db' not in g:
        g.db = sqlite3.connect(
            current_app.config['DATABASE'],
            detect_types=sqlite3.PARSE_DECLTYPES
        )
        g.db.row_factory = sqlite3.Row

    return g.db

def close_db(e=None):
    db = g.pop('db', None)

    if db is not None:
        db.close()

# Run the SQL Commands
def init_db():
    db = get_db()
    with current_app.open_resource('schema.sql') as f:
        db.executescript(f.read().decode('utf-8'))

@click.command('init-db')
@with_appcontext
def init_db_command():
    # Clear exisiting data and create new tables
    init_db()
    click.echo('Intialized database!')

'''
app.teardown_appcontext(): Tells flask to call that function once the response of the request is given
app.cli.add_command(): Adds a command which we can called with flask command
'''
# Register with an application
def init_app(app):
    app.teardown_appcontext(close_db)
    app.cli.add_command(init_db_command)
