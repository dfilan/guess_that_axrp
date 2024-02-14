from flask import (
    Blueprint, redirect, render_template, request, session, url_for,
)

from guess_that_axrp.db import get_db

bp = Blueprint('leaderboard', __name__, url_prefix='/leaderboard')

@bp.route('/')
def index():
    # get stuff from the db
    # sort by laplace_estimator
    # pick out top 20, and also the user's entry.
    db = get_db()
    my_uuid = "None" if 'uuid' not in session else session['uuid']
    with get_db() as conn:
        leaderboard = conn.execute(
            'SELECT * FROM (SELECT RANK() OVER(ORDER BY laplace_estimator DESC) as rank, '
            'username, uuid, successes, attempts, laplace_estimator, submitted FROM scores) '
            'WHERE rank <= 20 OR uuid = %s',
            (my_uuid,)
        ).fetchall()
    # send it to the template
    filtered_leaderboard = [
        {
            'rank': row['rank'],
            'username': row['username'],
            'successes': row['successes'],
            'attempts': row['attempts'],
            'laplace_estimator': round(row['laplace_estimator'], 3),
            'submitted': row['submitted']
        } for row in leaderboard
    ]
    return render_template('leaderboard/index.html', leaderboard=filtered_leaderboard)


@bp.route('/submit', methods=('GET', 'POST'))
def submit():
    if request.method == 'POST':
        # if we're posting, get data from the session + the user name,
        # calculate the laplace estimator, and get a timestamp, and send to the db.
        # then display the leaderboard.
        username = request.form['username']
        successors = session['correct_guesses']
        attempts = session['total_guesses']
        laplace = (successors + 1) / (attempts + len(session['ep_names']))
        db = get_db()
        with get_db() as conn:
            cur = conn.execute(
                'INSERT INTO scores (username, uuid, successes, attempts, laplace_estimator)'
                ' VALUES (%s, %s, %s, %s, %s)',
                (username, session['uuid'], successors, attempts, laplace)
            )
        return redirect(url_for('leaderboard.index'))
    else:
        # if we're getting, render the template, which should have a field for name,
        # a checkbox saying "I promise I didn't cheat", and a submit button.
        return render_template('leaderboard/submit.html')
