from flask import render_template
from app.accounts import bp
from app.extensions import db
from app.models.accounts import User


@bp.route('/')
def index():
    return render_template('accounts/index.html')
