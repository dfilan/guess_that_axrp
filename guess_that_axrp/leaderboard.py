from flask import Blueprint, render_template

bp = Blueprint('leaderboard', __name__, url_prefix='/leaderboard')

@bp.route('/')
def index():
    return render_template('leaderboard/index.html')


@bp.route('/submit', methods=('GET', 'POST'))
def submit():
    return render_template('leaderboard/submit.html')
