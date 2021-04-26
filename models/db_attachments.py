import sqlite3
import uuid
from datetime import datetime as dt


def get_connection() -> (sqlite3.Connection, sqlite3.Cursor):
    connection = sqlite3.connect('data/database.db')
    connection.execute("PRAGMA foreign_keys = ON;")
    return connection, connection.cursor()


class User:
    """
    Represents a user on the forum

    :param handle: The user's handle that they register with
    :type handle: str
    """

    def __init__(self, handle):
        if type(handle) is str:
            self.user_id = None    # User's database key
            self.fname = None       # User's first name
            self.lname = None       # User's last name
            self.handle = handle    # User's tag visible to all
            self.user_hash = None   # Unique user identifier

        if self.user_exists():
            self.acquire_user()
        else:
            self.init_user()

    @staticmethod
    def savealluser(fpath):
        conn, cur = get_connection()
        cur.execute("""SELECT * FROM User""")
        result = cur.fetchall()

        with open(fpath, "w") as f:
            f.writelines([f'{r[0]}\t{r[1]}\t{r[2]}\t{r[3]}\t{r[4]}\t{r[5]}\n' for r in result])

    @classmethod
    def get_user_from_hash(cls, user_hash: uuid.UUID):
        conn, cur = get_connection()
        cur.execute("""SELECT handle FROM User WHERE hash = ?""",
                    (str(user_hash),))
        result = cur.fetchall()
        if len(result) == 0:
            raise KeyError("User does not exist")
        return cls(result[0][0])

    # Checks if this user exists
    def user_exists(self) -> bool:
        conn, cur = get_connection()
        cur.execute("SELECT * FROM User WHERE handle = ?", (self.handle,))
        if len(cur.fetchall()) > 0:
            return True
        else:
            return False

    # Updates user's properties
    def acquire_user(self):
        if not self.user_exists():
            raise KeyError("User does not exist")
        conn, cur = get_connection()
        cur.execute("""
        SELECT user_id, first_name, last_name, hash FROM User where handle = ?
        """, (self.handle,))
        results = cur.fetchall()[0]

        # may need to update these when db schema is finalized
        self.user_id = results[0]
        self.fname = results[1]
        self.lname = results[2]
        self.user_hash = uuid.UUID(results[3])

    def init_user(self, *args):
        # *args may have fname, lastname
        self._make_hash()
        # self._set_names(fname, lname)
        self._create_user()

    def _create_user(self):
        if self.user_exists():
            raise KeyError("Trying to create user that already exists")

        conn, cur = get_connection()
        cur.execute("""
        INSERT INTO User(first_name, last_name, handle, hash) VALUES (?, ?, ?, ?)
        """, (self.fname, self.lname, self.handle, str(self.user_hash)))
        conn.commit()
        self.user_id = cur.lastrowid

    def _make_hash(self):
        self.user_hash = uuid.uuid4()

    def _set_names(self, fname, lname):
        self.fname = fname
        self.lname = lname


class Post:
    """
    A post representation

    Pass either an integer post id (if it exists) or a dictionary

    :argument post_id: Post's id
    :type post_id: int

    :keyword title: Title of a post
    :type post_title: str
    :keyword content: Content of post
    :type post_content: str
    :keyword creator: Creator of post
    :type post_creator: User

    :raises ValueError
    """

    def __init__(self, *args, **kwargs):
        if len(args) == 1 and type(args[0]) is int:
            self.post_id = args[0]
            self._acquire_post()
        elif len(kwargs) == 3:
            self.post_id = None
            self.post_title = kwargs['title']
            self.post_content = kwargs['content']
            self.post_creator = kwargs['creator']
            self.post_votes = 0
            self._create_post()
        else:
            raise ValueError("Must pass either post id or title. content, creator to instantiate a Post")

    def _create_post(self):
        conn, cur = get_connection()
        cur.execute("""
        INSERT INTO Post(title, content, post_user_id) VALUES(?, ?, ?)
        """, (self.post_title, self.post_content, self.post_creator.user_id))
        self.post_id = cur.lastrowid

        conn.commit()

    @staticmethod
    def saveallpost(fpath):
        conn, cur = get_connection()
        cur.execute("""SELECT * FROM Post""")
        result = cur.fetchall()

        with open(fpath, "w") as f:
            f.writelines([f'{r[0]}\t{r[1]}\t{r[2]}\t{r[3]}\t{r[4]}\n' for r in result])

    def _get_time_passed(self):
        td = dt.utcnow() - dt.fromisoformat(self.post_timestamp)
        if td.seconds < (60 * 60 * 24):
            minutes_ago = td.seconds // 60
            thirty_minutes_ago = minutes_ago // 30

            approximate_minutes = thirty_minutes_ago * 30
            if approximate_minutes == 0:
                self.time_passed = "Less than 30 Minutes Ago"
            else:
                self.time_passed = f"Approximately {approximate_minutes} Minutes Ago"
        else:
            self.time_passed = f"Approximately {td.seconds // (60 * 60 * 24)} Days Ago"

    def _acquire_post(self):
        conn, cur = get_connection()
        cur.execute("""
        SELECT p.title, p.content, u.handle, p.time_stamp 
        FROM Post p INNER JOIN User u ON u.user_id = p.post_user_id
        WHERE p.post_id = ?
        """, (self.post_id,))
        result = cur.fetchall()
        if len(result) == 0:
            raise KeyError("Post not found")

        self.post_title, self.post_content, creator, self.post_timestamp = result[0]
        self.post_creator = User(creator)
        self._get_time_passed()

        cur.execute("""
        SELECT SUM(v.weight) from Vote v WHERE v.vote_post_id = ?""", (self.post_id,))
        self.post_votes = cur.fetchall()[0][0]
        if self.post_votes is None:
            self.post_votes = 0

    def delete_post(self):
        con, cur = get_connection()
        cur.execute("""
        DELETE FROM Post WHERE post_id = ?
        """, (self.post_id,))
        con.commit()

class Vote:
    def __init__(self, voter: User, post: Post, vote: int):
        self.voter = voter
        self.post = post
        self.vote_id = -1

        if not ((vote == 1) or (vote == -1)):
            raise ValueError("Post vote weight must be either +1 (Up) or -1 (Down)")

        self.vote = vote

        if self.vote_exits():
            self._update_vote()
        else:
            self._create_vote()

    def vote_exits(self):
        conn, cur = get_connection()
        cur.execute("""
        SELECT vote_id FROM Vote WHERE vote_user_id = ? and vote_post_id = ?
        """, (self.voter.user_id, self.post.post_id))
        results = cur.fetchall()
        if len(results) != 0:
            self.vote_id = results[0][0]
            return True
        else:
            return False

    @staticmethod
    def saveallvote(fpath):
        conn, cur = get_connection()
        cur.execute("""SELECT * FROM Vote""")
        result = cur.fetchall()

        with open(fpath, "w") as f:
            f.writelines([f'{r[0]}\t{r[1]}\t{r[2]}\t{r[3]}\n' for r in result])

    def _create_vote(self):
        conn, cur = get_connection()
        cur.execute("""
        INSERT INTO Vote(vote_user_id, vote_post_id, weight) VALUES (?, ?, ?)
        """, (self.voter.user_id, self.post.post_id, self.vote))
        conn.commit()
        self.vote_id = cur.lastrowid

    def _update_vote(self):
        conn, cur = get_connection()
        cur.execute("""
        UPDATE Vote SET weight = ? WHERE vote_id = ?
        """, (self.vote, self.vote_id))

        conn.commit()


def get_profile_posts(user_hash: uuid.UUID) -> [Post]:
    u = User.get_user_from_hash(user_hash)
    conn, cur = get_connection()

    cur.execute("""
    SELECT p.post_id FROM Post p INNER JOIN User u ON p.post_user_id = u.user_id WHERE u.handle = ? 
    ORDER BY p.time_stamp DESC
    """, (u.handle,))

    return [Post(i[0]) for i in cur.fetchall()]


def get_feed_posts(user_hash: uuid.UUID) -> [Post]:
    u = User.get_user_from_hash(user_hash)
    conn, cur = get_connection()
    cur.execute("""
    SELECT p.post_id FROM Post p 
    INNER JOIN User u ON p.post_user_id = u.user_id
    WHERE u.handle != ?
    ORDER BY p.time_stamp DESC
    """, (u.handle,))

    return [Post(i[0]) for i in cur.fetchall()]
