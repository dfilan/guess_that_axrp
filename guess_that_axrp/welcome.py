from flask import Blueprint, render_template

bp = Blueprint('welcome', __name__)

@bp.route('/')
def index():
    return render_template('welcome/index.html')
