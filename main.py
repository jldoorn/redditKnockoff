import flask
from http import HTTPStatus
from models import db_attachments as db
import uuid

app = flask.Flask(__name__, static_folder="scripts")

@app.route("/api/register", methods=['GET', 'POST'])
def api_register():
    if flask.request.method == 'GET':
        return flask.render_template("register.html")
    elif flask.request.method == 'POST':
        data = flask.request.get_json()
        user = db.User(data['handle'])
        return {'user_hash': user.user_hash}
    else:
        return flask.abort(HTTPStatus.NOT_IMPLEMENTED)

@app.route("/register", methods=['GET', 'POST'])
def register():
    if flask.request.method == 'GET':
        return flask.render_template("register.html")
    elif flask.request.method == "POST":
        handle = flask.request.form['handle']
        user = db.User(handle)
        return flask.redirect(f'/{user.user_hash}/profile')

@app.route("/<user_hash>/feed", methods=['GET'])
def feed(user_hash):
    try:
        posts = db.get_feed_posts(user_hash)
    except KeyError:
        return flask.abort(404)

    # return flask.jsonify([{
    #     'post_title': p.post_title,
    #     'post_content': p.post_content,
    #     'post_creator': p.post_creator.handle,
    #     'post_timestamp': p.post_timestamp,
    #     'post_id': p.post_id
    # } for p in posts])
    return flask.render_template('feed.html', user_hash=user_hash, posts=posts)


@app.route("/posts/<post_id>", methods=['GET'])
def post(post_id):
    try:
        p = db.Post(int(post_id))
    except KeyError:
        return flask.abort(404)

    # return {
    #     'post_id': p.post_id,
    #     'post_timestamp': p.post_timestamp,
    #     'post_creator': p.post_creator.handle,
    #     'post_title': p.post_title,
    #     'post_content': p.post_content,
    #     "post_votes": p.post_votes
    # }
    return flask.render_template("post.html", post=p)


@app.route("/<user_hash>/profile", methods=['GET'])
def profile(user_hash):
    try:
        posts = db.get_profile_posts(user_hash)
    except KeyError:
        return flask.abort(404)

    return flask.render_template("profile.html", posts=posts, user_hash=user_hash)

@app.route("/<user_hash>/vote/<post_id>/<direction>", methods=['GET'])
def postVote(user_hash, post_id, direction):
    if direction == "up":
        db.Vote(db.User.get_user_from_hash(uuid.UUID(user_hash)), db.Post(int(post_id)), 1)
        return flask.redirect("/"+user_hash+"/feed")
    elif direction == "down":
        db.Vote(db.User.get_user_from_hash(uuid.UUID(user_hash)), db.Post(int(post_id)), -1)
        return flask.redirect("/" + user_hash + "/feed")
    else:
        return flask.abort(404)

@app.route("/api/<user_hash>/profile", methods=['GET'])
def api_profile(user_hash):
    posts = db.get_profile_posts(user_hash)
    return flask.jsonify([{
        'post_title': p.post_title,
        'post_content': p.post_content,
        'post_creator': p.post_creator.handle,
        'post_timestamp': p.post_timestamp,
        'post_id': p.post_id
    } for p in posts])

@app.route("/api/<user_hash>/feed", methods=['GET'])
def api_feed(user_hash):
    try:
        posts = db.get_feed_posts(user_hash)
    except KeyError:
        return flask.abort(404)

    return flask.jsonify([{
        'handle': p.post_creator.handle,
        'post_votes': p.post_votes,
        'post_title': p.post_title,
        'post_content': p.post_content,
        'post_creator': p.post_creator.handle,
        'post_timestamp': p.post_timestamp,
        'post_id': p.post_id,
        'time_passed': p.time_passed
    } for p in posts])

@app.route("/<user_hash>/delete/<post_id>", methods=["POST"])
def delete_post(user_hash, post_id):
    p = db.Post(int(post_id))
    if p.post_creator.user_hash == uuid.UUID(user_hash):
        p.delete_post()

    return flask.redirect(f'/{user_hash}/profile')


@app.route("/<user_hash>/create", methods=['GET','POST'])
def create(user_hash):
    if flask.request.method == "GET":
        return flask.render_template("create.html", user_hash=user_hash)
    else:
        user = db.User.get_user_from_hash(uuid.UUID(user_hash))
        # data = flask.request.get_json()
        db.Post(content=flask.request.form['post_content'], title=flask.request.form['post_title'], creator=user)
        return flask.redirect(f'/{user_hash}/profile')

@app.route("/", methods=['GET'])
def root():
    return flask.redirect("/register")

@app.route("/app", methods=['GET'])
def apprt():
    return flask.render_template("app.html")

if __name__ == '__main__':
    app.run(port=8000, host='127.0.0.1', debug=True, use_evalex=False)