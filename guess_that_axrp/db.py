import os

import click
from flask import current_app
import psycopg
import requests


def get_db():
    con = psycopg.connect(
        current_app.config['DATABASE_URL'],
        row_factory=psycopg.rows.dict_row,
    )

    return con


def get_axrp_files():
    # get the contents of the _posts directory of the axrp.github.io repo
    repo_posts_url = "https://api.github.com/repos/axrp/axrp.github.io/contents/_posts"
    auth_header = {"Authorization": f"token {current_app.config['GITHUB_TOKEN']}"}
    response = requests.get(repo_posts_url, headers=auth_header)
    files = response.json()
    # download each file that's an episode
    raw_prefix = "https://raw.githubusercontent.com/axrp/axrp.github.io/master/_posts/"
    episode_texts = []
    for file_dict in files:
        file_name = file_dict['name']
        # file name has got to contain "episode-[number]", the number can't be 7.5 (aka can't
        # be followed by an underscore), and it's got to end in ".markdown"
        if "episode-" in file_name and not "7_5" in file_name and file_name.endswith(".markdown"):
            file_url = raw_prefix + file_name
            response = requests.get(file_url, headers=auth_header)
            episode_texts.append(response.text)

    return episode_texts           

        
def init_db():
    """Initialize the database and populate it with the AXRP episodes."""
    with get_db() as con:
        with current_app.open_resource('schema.sql') as f:
            con.execute(f.read().decode('utf8'))

        # call a thing to get files from the AXRP website
        # the title is the first bit of the text after "title: " in quotes
        ep_texts = get_axrp_files()
        for ep_text in ep_texts:
            title = ep_text.split("title:")[1].lstrip().split("\"")[1]
            try:
                cur = con.execute(
                    'INSERT INTO episodes (title, contents) VALUES (%s, %s)',
                    (title, ep_text)
                )
            except psycopg.IntegrityError:
                error = f"Episode {title} is already in the database."
                flash(error)


@click.command('init-db')
def init_db_command():
    """Clear the existing data and create new tables"""
    init_db()
    click.echo('Initialized the database.')


def init_app(app):
    app.cli.add_command(init_db_command)
