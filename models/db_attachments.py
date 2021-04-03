import sqlite3
import uuid
import time


def get_connection() -> (sqlite3.Connection, sqlite3.Cursor):
    connection = sqlite3.connect('database.db')
    return connection, connection.cursor()


class User:
    """
    Represents a user on the forum

    :param handle: The user's handle that they register with
    :type handle: str
    """

    def __init__(self, handle):
        self.user_id = None    # User's database key
        self.fname = None       # User's first name
        self.lname = None       # User's last name
        self.handle = handle    # User's tag visible to all
        self.user_hash = None   # Unique user identifier

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
        conn, cur = get_connection()
        cur.execute("""
        SELECT * FROM User where handle = ?
        """, (self.handle,))
        results = cur.fetchall()[0]

        # may need to update these when db schema is finalized
        self.user_id = results[0]
        self.fname = results[1]
        self.lname = results[2]
        self.user_hash = results[3]

    def init_user(self, fname, lname):
        self._make_hash()
        self._set_names(fname, lname)
        self._create_user()

    def _create_user(self):
        if self.user_exists():
            raise KeyError("Trying to create user that already exists")

        conn, cur = get_connection()
        cur.execute("""
        INSERT INTO User(fname, lname, handle, hash) VALUES (?, ?, ?, ?)
        """, (self.fname, self.lname, self.handle, self.user_hash))
        conn.commit()

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
        elif len(kwargs) == 3:
            self.post_id = 0
            self.post_title = kwargs['title']
            self.post_content = kwargs['content']
            self.post_creator = kwargs['creator']
        else:
            raise ValueError("Must pass either post id or title. content, creator to instantiate a Post")

    def _create_post(self):
        conn, cur = get_connection()
        cur.execute("""
        INSERT INTO Post(title, content, user_id) VALUES(?, ?, ?)
        """, (self.post_title, self.post_content, self.post_creator.user_id))
        self.post_id = cur.lastrowid

        conn.commit()
