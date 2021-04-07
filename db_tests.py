import unittest
from models import db_attachments as db


class TestDB(unittest.TestCase):

    def setUp(self) -> None:
        conn, cur = db.get_connection()
        cur.execute("""
        DELETE FROM Post
        """)
        cur.execute("""DELETE FROM User""")
        cur.execute("""DELETE FROM Vote""")
        conn.commit()

    def test_user(self):

        with self.subTest('create user'):
            userInit = db.User('technojd')
            self.assertEqual(userInit.user_id, 'technojd')
            self.assertIsNotNone(userInit.user_hash)
            self.assertIsNotNone(userInit.user_id)

        with self.subTest('reAccess user'):
            userOld = db.User('technojd')
            self.assertEqual(userOld.user_id, userInit.user_id)
            self.assertEqual(userOld.user_hash, userInit.user_hash)

    def test_post(self):

        with self.subTest('create post'):
            newPost = db.Post(title='New Post', content='Today a first post', creator=db.User('technojd'))
            self.assertIsNotNone(newPost.post_id)

        with self.subTest('recall post'):
            oldPost = db.Post(newPost.post_id)
            self.assertEqual(newPost.post_content, oldPost.post_content)


if __name__ == '__main__':
    unittest.main()
