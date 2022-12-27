#!/usr/bin/python3
"""Blueprint to capture the authentication details.
"""
import functools

from flask import (
    Blueprint, flash, g, redirect, render_template, request, session,
    url_for
)
import uuid
from werkzeug.security import check_password_hash, generate_password_hash
from ..db import get_db


auth_views = Blueprint('auth', __name__, url_prefix='/auth')


@auth_views.route('/register', methods=('GET', 'POST'),
                  strict_flashes=False)
def register():
    """Return a form for users to fill out."""
    if request.method == 'POST':
        first_name = request.form['first name']
        last_name = request.form['last name']
        email = request.form['email']
        passwd = request.form['password']
        birthday = request.form['birthday']
        user_type = request.form['category']

        db = get_db()
        error = None
        user_id = str(uuid.uuid4())

        if not first_name:
            error = 'First name is required'
        elif not last_name:
            error = 'Last name is required'
        elif not email:
            error = 'Email is required.'
        elif not passwd:
            error = 'Password is required.'
        elif not birthday:
            error = 'Birthday is required.'
        elif not user_type:
            error = 'Category selection is required.'

        if user_type == 'professional':
            user_type = 'P'
        elif user_type == 'student':
            user_type = 'S'

        if error is None:
            try:
                query = """
                INSERT INTO user (user_id, first_name, last_name, email,
                passwd, birthday, user_type) VALUES (?, ?, ?, ?, ?, ?, ?)
                """
                db.execute(query, (user_id, first_name, last_name, email,
                           generate_password_hash(passwd), birthday,
                           user_type)
                           )
                db.commit()
            except db.IntegrityError:
                error = f"User {email} is already registered."
            else:
                return redirect(url_for('auth.login'))
        flash(error)
    return render_template('auth/register.html')


@auth_views.route('/login', methods=('GET, POST'), strict_slashes=False)
def login():
    """Facilitate the logining in of users."""
    if request.method == 'POST':
        email = request.form['email']
        passwd = request.form['password']

        db = get_db()
        error = None

        query = """SELECT * FROM user WHERE email = ?"""
        user = db.execute(query, (email, )).fetchone()

        if user is None:
            error = 'Incorrect email.'
        elif not check_password_hash(user['passwd'], passwd):
            error = 'Incorrect password.'

        if error is None:
            session.clear()
            session['user_id'] = user['user_id']
            return redirect(url_for('index'))

        flash(error)
    return render_template('auth/login.html')


@auth_views.route('/logout', strict_slashes=False)
def logout():
    """Removes the `user_id` from the session.

    This ensures that the function `load_logged_in_user` does not
    load a user on subsequent requests.
    """
    session.clear()
    return redirect(url_for('index'))


@auth_views.before_app_request
def load_logged_in_user():
    """Runs before any view function whose URL is requested."""
    user_id = session.get('user_id')

    if user_id is None:
        g.user = None
    else:
        query = "SELECT * FROM user WHERE user_id = ?"
        g.user = get_db().execute(query, (user_id, )).fetchone()


def login_required(view):
    """Return a new view function that wraps the original view.

    Decorator that checks whether a user is logged in to perform
    certain actions on the app.
    """
    @functools.wraps(view)
    def wrapped_view(**kwargs):
        if g.user is None:
            return redirect(url_for('auth.login'))
        return view(**kwargs)

    return wrapped_view
