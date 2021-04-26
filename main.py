import flask
from http import HTTPStatus
from models import db_attachments as db
import uuid
import os

app = flask.Flask(__name__, static_folder="static")
app.config['CLIENT_TSV'] = './data/tsvfiles'
app.config['CLIENT_IMAGE'] = './data/uploads'

@app.route("/register", methods=['GET', 'POST'])
def register():
    if flask.request.method == 'GET':
        return flask.render_template("register.html")
    elif flask.request.method == "POST":
        handle = flask.request.form['handle']
        file = flask.request.files['profpic']
        user = db.User(handle)
        if file.filename != "":
            filename = f'{user.user_hash}.png'
            file.save(os.path.join(app.config['CLIENT_IMAGE'], filename))
        return flask.redirect(f'/app/feed/{user.user_hash}')

@app.route("/posts/<post_id>", methods=['GET'])
def post(post_id):
    try:
        p = db.Post(int(post_id))
    except KeyError:
        return flask.abort(404)

    return flask.render_template("post.html", post=p)

@app.route("/<user_hash>/vote/<post_id>/<direction>", methods=['GET'])
def postVote(user_hash, post_id, direction):
    if direction == "up":
        db.Vote(db.User.get_user_from_hash(uuid.UUID(user_hash)), db.Post(int(post_id)), 1)
        return {
            "tally": db.Post(int(post_id)).post_votes
        }
    elif direction == "down":
        db.Vote(db.User.get_user_from_hash(uuid.UUID(user_hash)), db.Post(int(post_id)), -1)
        return {
                    "tally": db.Post(int(post_id)).post_votes
                }
    else:
        return flask.abort(404)

@app.route("/api/<user_hash>/profile", methods=['GET'])
def api_profile(user_hash):
    posts = db.get_profile_posts(user_hash)
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

@app.route("/api/<user_hash>/delete/<post_id>", methods=['GET'])
def api_delete_post(user_hash, post_id):
    p = db.Post(int(post_id))
    if p.post_creator.user_hash == uuid.UUID(user_hash):
        p.delete_post()

    return {
        "status": "ok"
    }

@app.route("/<user_hash>/create", methods=['GET','POST'])
def create(user_hash):
    if flask.request.method == "GET":
        return flask.render_template("create.html", user_hash=user_hash)
    else:
        user = db.User.get_user_from_hash(uuid.UUID(user_hash))
        # data = flask.request.get_json()
        db.Post(content=flask.request.form['post_content'], title=flask.request.form['post_title'], creator=user)
        return flask.redirect(f'/app/profile/{user_hash}')

@app.route("/", methods=['GET'])
def root():
    return flask.redirect("/register")

@app.route("/app/profile/<user_hash>", methods=['GET'])
def apprtprofile(user_hash):
    return flask.render_template("app.html", user_hash=user_hash, feed=False)

@app.route("/app/feed/<user_hash>", methods=['GET'])
def apprtfeed(user_hash):
    return flask.render_template("app.html", user_hash=user_hash, feed=True)

@app.route("/gettsv", methods=['GET'])
def tsvpage():
    return flask.render_template("gettsv.html")


@app.route("/gettsv/<tsvtype>", methods=['GET'])
def tsvdownload(tsvtype):
    if tsvtype == 'user':
        db.User.savealluser('data/tsvfiles/user.tsv')
        return flask.redirect('/gettsv/download/user.tsv')
    elif tsvtype == 'post':
        db.Post.saveallpost('data/tsvfiles/post.tsv')
        return flask.redirect('/gettsv/download/post.tsv')
    elif tsvtype == 'vote':
        db.Vote.saveallvote('data/tsvfiles/vote.tsv')
        return flask.redirect('/gettsv/download/vote.tsv')
    else:
        return flask.abort(404)

@app.route("/gettsv/download/<path:tsvpath>", methods=['GET'])
def downloadpath(tsvpath):
    return flask.send_from_directory(app.config['CLIENT_TSV'], tsvpath)

@app.route("/image/<path:imagepath>")
def getimage(imagepath):
    return flask.send_from_directory(app.config['CLIENT_IMAGE'], imagepath)

if __name__ == '__main__':
    app.run(port=8000, host='127.0.0.1', debug=True, use_evalex=False)