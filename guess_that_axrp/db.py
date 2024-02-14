import sqlite3

import click
from flask import current_app, g
import requests


def get_db():
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


def get_axrp_files():
    # get the contents of the _posts directory of the axrp.github.io repo
    response = requests.get("https://api.github.com/repos/axrp/axrp.github.io/contents/_posts")
    files = response.json()
    # download each file that's an episode
    raw_prefix = "https://raw.githubusercontent.com/axrp/axrp.github.io/master/_posts/"
    episode_texts = []
    for file_dict in files:
        print(file_dict)
        file_name = file_dict['name']
        # file name has got to contain "episode-[number]", the number can't be 7.5 (aka can't
        # be followed by an underscore), and it's got to end in ".markdown"
        if "episode-" in file_name and not "7_5" in file_name and file_name.endswith(".markdown"):
            file_url = raw_prefix + file_name
            response = requests.get(file_url)
            episode_texts.append(response.text)

    return episode_texts           

        
def init_db():
    """Initialize the database and populate it with the AXRP episodes."""
    db = get_db()

    with current_app.open_resource('schema.sql') as f:
        db.executescript(f.read().decode('utf8'))

    # call a thing to get files from the AXRP website
    # ok and the title is the first bit of the text after "title: " in quotes
    ep_texts = get_axrp_files()
    for ep_text in ep_texts:
        title = ep_text.split("title:")[1].lstrip().split("\"")[1]
        try:
            db.execute(
                'INSERT INTO episodes (title, contents) VALUES (?, ?)',
                (title, ep_text)
            )
            db.commit()
        except sqlite3.IntegrityError:
            error = f"Episode {title} is already in the database."
            flash(error)


@click.command('init-db')
def init_db_command():
    """Clear the existing data and create new tables"""
    init_db()
    click.echo('Initialized the database.')


def init_app(app):
    app.teardown_appcontext(close_db)
    app.cli.add_command(init_db_command)
    # init_db()
    # so I can't initialize the db right away because I don't have the app context yet
    # so do I have to do that manually, once the app is created?
    # wait why am I even doing this whole application factory thing?
    # whatever I'm sure it's fine
