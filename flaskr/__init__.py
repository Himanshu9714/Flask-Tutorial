import os
from flask import Flask

def create_app(test_config=None):
    # Creates a class instance
    app = Flask(__name__, instance_relative_config=True)  

    '''
    app.config.from_mapping() sets default configuration which will be used by app
    SECRET_KEY: Keep data safe and used by flask and extensions
    DATABASE: Path of SQLite Database
    '''
    app.config.from_mapping(
        SECRET_KEY='dev',
        DATABASE=os.path.join(app.instance_path, 'flaskr.sqlite'),
    )

    '''
    app.config.from_pyfile(): Overrides default configuration with values taken from config.py file 
        => For eg, set the real value of SECRET_KEY during deployment
    '''
    if test_config is None:
        app.config.from_pyfile('config.py', silent=True)
    else:
        app.config.from_mapping(test_config)

    try:
        os.makedirs(app.instance_path)
    except OSError:
        pass

    @app.route('/hello')
    def hello():
        return 'Hello, World!'
    
    from . import db
    db.init_app(app)

    from . import auth
    app.register_blueprint(auth.bp)

    from . import blog
    app.register_blueprint(blog.bp)
    app.add_url_rule('/', endpoint='index')

    return app
