import os

from flask import Flask

def create_app(test_config=None):
    # create and configure the app
    app = Flask(__name__, instance_relative_config=True)
    app.config.from_mapping(
        SECRET_KEY='dev', # should override this with a random value when deploying
        DATABASE=os.path.join(app.instance_path, 'guess_that_axrp.sqlite'),
    )

    if test_config is None:
        # load the instance config, if it exists, when not testing
        # so this could override SECRET_KEY
        app.config.from_pyfile('config.py', silent=True)
    else:
        # load the test config if passed in
        app.config.from_mapping(test_config)

    # ensure the instance folder exists
    try:
        os.makedirs(app.instance_path)
    except OSError:
        pass

    from . import db
    db.init_app(app)

    from . import guess
    app.register_blueprint(guess.bp)
    app.add_url_rule('/', endpoint='index')

    return app
