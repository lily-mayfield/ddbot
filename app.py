# TODO: rename this view.py? put app factory in another file?
import requests
from flask import (
    Flask, redirect, render_template, url_for, send_from_directory, request, send_file, jsonify, make_response
)

from . import config
from . import models
from . import moderate
from . import templating


app = Flask(__name__)
app.config.from_object(config)


@app.route("/proposals", methods=['GET'])
def view_proposals():
    """View proposals by timestamp in a list.

    """

    # full text search
    search_for_this_text = request.args.get('search')
    if search_for_this_text:
        like_query = '%' + search_for_this_text + '%'
        posts = (
            models.Post.query.filter(
                models.Post.message.like(like_query),
            )
            .order_by(models.Post.bumptime.desc())
            .all()
        )
    else:
        posts = (
            models.Post.query.filter(models.Post.reply_to == None)
            .order_by(models.Post.bumptime.desc())
            .all()
        )

    for post in posts:
        reply_query = (
            models.Post.query
            .filter(models.Post.reply_to == post.id)
        )
        post.reply_count = reply_query.count()
        post.last_reply = reply_query.order_by(models.Post.bumptime.desc()).first()

    return render_template(
        'list.html',
        form=forms.NewPostForm(),
        posts=posts,
    )


with app.app_context():
    # Create admin
    admin_ = Admin(app, 'Example: Auth', index_view=moderate.MyAdminIndexView(), base_template='my_master.html')
    models.db.init_app(app)
    moderate.build_sample_db()
