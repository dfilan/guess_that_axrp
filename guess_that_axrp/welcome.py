from flask import Blueprint, render_template

from guess_that_axrp.db import get_db

bp = Blueprint('welcome', __name__)

@bp.route('/')
def index():
    return render_template('welcome/index.html')
