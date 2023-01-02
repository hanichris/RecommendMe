#!/usr/bin/python3
"""View to support creation, updation, deletion of posts."""
from datetime import datetime
from flask import (
    Blueprint, flash, g, redirect, render_template, request, url_for
)
from uuid import uuid4
from werkzeug.exceptions import abort
from .auth import login_required
from ..db import get_db


post_views = Blueprint('post', __name__)


@post_views.route('/', methods=['GET', 'POST'])
def index():
    """View for the homepage of the web app."""
    if request.method == 'POST':
        status = request.form['status']

        error = None

        if not status:
            error = 'Status is empty!'

        if error is not None:
            flash(error)
        else:
            post_id = str(uuid4())
            created_at = datetime.now()
            query = """
            INSERT INTO post (post_id, author_id, created_at, body)
            VALUES (?, ?, ?, ?)
            """

            db = get_db()
            try:
                db.execute(query, (post_id, g.user['user_id'],
                           created_at.isoformat(timespec='milliseconds'),
                           status))

                db.commit()
            except db.IntegrityError as err:
                print(f'Error {err=} of type {type(err)=}')
            else:
                redirect(url_for('post.index'))
        return render_template('post/index.html')

    elif request.method == 'GET':
        db = get_db()
        query = """
        SELECT username, created_at, body FROM post p INNER
        JOIN user u ON p.author_id = u.user_id
        ORDER BY created_at DESC
        """

        posts = db.execute(query).fetchall()
        return render_template('post/index.html', posts=posts)
