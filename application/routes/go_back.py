"""
    This file contains all views handling going back
"""

from flask import (
    Blueprint, flash, g, redirect, render_template, request, url_for, jsonify
)
from flask_login import login_required, current_user
from .page_stack import PageStack

# Create blueprint for deck views
bp = Blueprint('go_back', __name__)

@bp.route('/go_back/from_file')
@login_required
def go_back():
    PageStack.previous()