"""
    This file contains all views for playing a deck.
"""

from flask import (
    Blueprint, flash, g, redirect, render_template, request, url_for
)
from flask_login import login_user

from application.auth import LoginForm, RegistrationForm
from application.handlers import Userhandler

# Create blueprint for deck views
bp = Blueprint('auth', __name__)

@bp.route('/auth/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    # Check if correct submitted login
    if not form.validate_on_submit():
        return render_template('auth/login.html', form=form)
    # Do the login
    username = form.username.data
    user = Userhandler.get_by_username(username)
    if user and user.check_password(form.password.data):
        login_user(user, remember=request.form.get('remember'))
        flash('Login successful')
        return redirect(url_for('decks.index'))
    else:
        flash('Login unsuccessful. Please check username and password')
    return redirect(url_for('auth.login'))


@bp.route('/auth/register', methods=['GET', 'POST'])
def register():
    form = RegistrationForm()
    # Check if correct submitted login
    if not form.validate_on_submit():
        return render_template('auth/register.html', form=form)
    # Do the login
    username = form.username.data
    email = form.email.data
    Userhandler.add_user(username, email, form.password.data)
    flash('Account created successfully. Proceed to log in')
    return redirect(url_for('auth.login'))

