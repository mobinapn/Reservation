from flask import render_template, redirect, url_for, request, flash
from flask_login import login_user, login_required, current_user, logout_user

from app.accounts import bp
from app.extensions import db
from app.models.accounts import User, Customer


@bp.route('/login')
def login():
    return render_template('accounts/login.html')

@bp.route('/login', methods=['POST'])
def login_post():
    phone = request.form.get('phone')
    password = request.form.get('password')

    if phone[0] != '9' or len(phone) != 10:
        flash('شماره تلفن شما باید متشکل از ده رقم بوده و با عدد نه شروع شود')
        return redirect(url_for('accounts.login'))

    user = User.query.filter_by(phone=phone).first()
    if not user or not user.check_password(password):
        flash('شماره تلفن یا رمز عبور اشتباه است')
        return redirect(url_for('accounts.login'))
    else:
        login_user(user)
        return redirect(url_for('main.index'))

@bp.route('/signup')
def signup():
    return render_template('accounts/signup.html')

@bp.route('/signup', methods=['POST'])
def signup_post():
    firstname = request.form.get('firstname')
    lastname = request.form.get('lastname')
    phone = request.form.get('phone')
    password = request.form.get('password')
    confirm = request.form.get('confirm')

    if phone[0] == '0' or len(phone) != 10:
        flash('شماره تلفن شما باید متشکل از ده رقم بوده و با عدد صفر شروع نشود')
        return redirect(url_for('accounts.signup'))
    elif password != confirm:
        flash('شما رمز عبور خود را به درستی تایید نکرده اید')
        return redirect(url_for('accounts.signup'))

    user = User.query.filter_by(phone=phone).first()
    if user:
        flash('کاربری با این شماره تلفن قبلا ثبت نام کرده است')
        return redirect(url_for('accounts.signup'))
    else:
        new_customer = Customer(firstname=firstname, lastname=lastname, phone=phone)
        new_customer.set_password(password)
        db.session.add(new_customer)
        db.session.commit()
        login_user(new_customer)
        return redirect(url_for('main.index'))


@bp.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('main.index'))
