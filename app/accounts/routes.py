from flask import render_template, redirect, url_for, request, flash
from flask_login import login_user, login_required, current_user, logout_user

from app.accounts import bp
from app.extensions import db
from app.models.accounts import User


@bp.route('/login')
def login():
    return render_template('accounts/login.html')

@bp.route('/login', methods=['POST'])
def login_post():
    pass

@bp.route('/signup')
def signup():
    return render_template('accounts/signup.html')

@bp.route('/signup', methods=['POST'])
def signup_post():
    pass

@bp.route('/logout')
@login_required
def logout():
    pass
