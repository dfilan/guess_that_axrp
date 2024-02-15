import functools
import random
import uuid

from flask import flash, redirect, session, url_for

from guess_that_axrp.db import get_db

def init_session():
    session.clear()
    session['uuid'] = str(uuid.uuid4())
    with get_db() as con:
        eps = con.execute('SELECT id, title FROM episodes').fetchall()
    names_and_ids = [(ep['title'], ep['id']) for ep in eps]
    names_and_ids.sort(key=lambda x: x[1])
    session['ep_names'] = [ep[0] for ep in names_and_ids]
    session['correct_guesses'] = 0
    session['total_guesses'] = 0
    session['playing'] = True

def end_session():
    session.clear()
    session['playing'] = False


def must_be_playing(view):
    @functools.wraps(view)
    def wrapped_view(**kwargs):
        if 'playing' not in session or not session['playing']:
            flash("You tried to access a page that requires you to have started the game."
                  + " Redirected to the main page.")
            return redirect(url_for('welcome.index'))

        return view(**kwargs)

    return wrapped_view
