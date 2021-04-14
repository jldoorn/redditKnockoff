import unittest
from models import db_attachments as db
import uuid

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
            self.assertEqual(userInit.handle, 'technojd')
            self.assertIsNotNone(userInit.user_hash)
            self.assertIsNotNone(userInit.user_id)

        with self.subTest('reAccess user'):
            userOld = db.User('technojd')
            self.assertEqual(userOld.user_id, userInit.user_id)
            self.assertEqual(userOld.user_hash, userInit.user_hash)

        with self.subTest('reAccess hash'):
            userHash = db.User.get_user_from_hash(userOld.user_hash)
            self.assertEqual(userOld.user_id, userHash.user_id)
            self.assertEqual(userOld.user_hash, userHash.user_hash)
            self.assertEqual(userOld.handle, userHash.handle)

        with self.subTest("invalid user"):
            with self.assertRaises(KeyError):
                db.User.get_user_from_hash(uuid.uuid4())


    def test_post(self):

        with self.subTest('create post'):
            newPost = db.Post(title='New Post', content='Today a first post', creator=db.User('technojd'))
            self.assertIsNotNone(newPost.post_id)

        with self.subTest('recall post'):
            oldPost = db.Post(newPost.post_id)
            self.assertEqual(newPost.post_content, oldPost.post_content)

        with self.subTest("invalid post"):
            with self.assertRaises(KeyError):
                db.Post(123456)

    def test_retreival(self):

        amanda = db.User('amanda')
        mary = db.User('mary')

        amandaPost1 = db.Post(title='First post', content='Amanda first post', creator=amanda)
        amandaPost2 = db.Post(title='Second post', content='Amanda second post', creator=amanda)

        maryPost1 = db.Post(title='First post', content='Mary first post', creator=mary)
        maryPost2 = db.Post(title='Second post', content='Mary second post', creator=mary)

        with self.subTest('check amanda posts'):
            amandaPosts = db.get_profile_posts(amanda.user_hash)
            self.assertEqual(amandaPost1.post_content, amandaPosts[0].post_content)
            self.assertEqual(amandaPost2.post_content, amandaPosts[1].post_content)

        with self.subTest('check mary posts'):
            maryPosts = db.get_profile_posts(mary.user_hash)
            self.assertEqual(maryPost1.post_content, maryPosts[0].post_content)
            self.assertEqual(maryPost2.post_content, maryPosts[1].post_content)

        with self.subTest('check feed posts amanda'):
            amandaFeedPosts = db.get_feed_posts(amanda.user_hash)
            # self.assertEqual(self.jdPost.post_content, amandaFeedPosts[0].post_content)
            self.assertEqual(len(amandaFeedPosts), 2)
            self.assertEqual(maryPost1.post_content, amandaFeedPosts[0].post_content)
            self.assertEqual(maryPost2.post_content, amandaFeedPosts[1].post_content)


if __name__ == '__main__':
    unittest.main()
