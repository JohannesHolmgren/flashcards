"""
    This file contains all views for playing a deck.
"""

from flask import (
    Blueprint, flash, g, redirect, render_template, request, url_for
)
from application.auth import LoginForm

# Create blueprint for deck views
bp = Blueprint('auth', __name__)

@bp.route('/auth/register')
def register():
    username = request.form.get('username')
    password = request.form.get('password')

@bp.route('/auth/login')
def login():
    form = LoginForm()