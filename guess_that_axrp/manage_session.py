import functools
import random
import uuid

from flask import Blueprint, flash, redirect, session, url_for

from guess_that_axrp.db import get_db

bp = Blueprint('manage_session', __name__, url_prefix='/manage_session')

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


@bp.route('/')
def end_session():
    session.clear()
    session['playing'] = False
    return redirect(url_for('welcome.index'))


def must_be_playing(view):
    @functools.wraps(view)
    def wrapped_view(**kwargs):
        if 'playing' not in session or not session['playing']:
            flash("You tried to access a page that requires you to have started the game."
                  + " Redirected to the main page.")
            return redirect(url_for('welcome.index'))

        return view(**kwargs)

    return wrapped_view
