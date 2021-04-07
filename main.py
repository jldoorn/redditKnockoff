import flask
from http import HTTPStatus
from models import db_attachments as db

app = flask.Flask(__name__)

@app.route("/register", methods=['GET', 'POST'])
def register():
    if flask.request.method == 'GET':
        return flask.render_template("register.html")
    elif flask.request.method == 'POST':
        user = db.User(flask.request.form['handle'])
        return {'user_hash': user.user_hash}
    else:
        return flask.abort(HTTPStatus.NOT_IMPLEMENTED)

@app.route("/<user_hash>/feed", methods=['GET'])
def feed(user_hash):
    posts = db.get_feed_posts(user_hash)

    return [{
        'post_title': p.post_title,
        'post_content': p.post_content,
        'post_creator': p.post_creator.handle,
        'post_timestamp': p.post_timestamp
    } for p in posts]
