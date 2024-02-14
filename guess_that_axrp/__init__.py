import os
# import threading
# import time

from flask import Flask

def create_app(test_config=None):
    # create and configure the app
    app = Flask(__name__, instance_relative_config=True)
    app.config.from_mapping(
        SECRET_KEY=os.environ['SECRET_KEY'],
        DATABASE_URL=os.environ['DATABASE_URL'],
        GITHUB_TOKEN=os.environ['GITHUB_TOKEN'],
    )

    if test_config is None:
        # load the instance config, if it exists, when not testing
        # so this could override SECRET_KEY
        app.config.from_pyfile('config.py', silent=True)
    else:
        # load the test config if passed in
        app.config.from_mapping(test_config)

    from . import db
    db.init_app(app)

    from . import welcome
    app.register_blueprint(welcome.bp)

    from . import guess
    app.register_blueprint(guess.bp)
    # app.add_url_rule('/', endpoint='index')

    from . import leaderboard
    app.register_blueprint(leaderboard.bp)

    # spawn a thread to update the database every some period of time
    # TODO figure out how to do that
    # write code to catch and print exceptions (flash????)
    # except CTRL-C when you should shut down.
    # x = threading.Thread(target=my_thread_function)
    # x.start()

    return app


# def my_thread_function():
#     print("Thread starting")
#     time.sleep(5)
#     print("Thread ending")
