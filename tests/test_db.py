import unittest

from xbot import db


class TestDb(unittest.TestCase):
    def setUp(self):
        self.conn = db.init_db(":memory:")

    def test_add_and_get(self):
        pid = db.add_post(self.conn, "hello", "learning")
        post = db.get_post(self.conn, pid)
        self.assertIsInstance(post, dict)
        self.assertEqual(post["text"], "hello")
        self.assertEqual(post["pillar"], "learning")
        self.assertEqual(post["status"], "drafted")
        self.assertTrue(post["created_at"])
        self.assertEqual(set(post), {"id", "text", "pillar", "status", "created_at"})

    def test_ids_increase(self):
        a = db.add_post(self.conn, "a", "p")
        b = db.add_post(self.conn, "b", "p")
        self.assertGreater(b, a)

    def test_invalid_status_on_add(self):
        with self.assertRaises(ValueError):
            db.add_post(self.conn, "x", "p", status="live")

    def test_set_status(self):
        pid = db.add_post(self.conn, "x", "p")
        db.set_status(self.conn, pid, "approved")
        self.assertEqual(db.get_post(self.conn, pid)["status"], "approved")
        with self.assertRaises(ValueError):
            db.set_status(self.conn, pid, "nope")

    def test_unknown_id(self):
        with self.assertRaises(KeyError):
            db.get_post(self.conn, 999)
        with self.assertRaises(KeyError):
            db.set_status(self.conn, 999, "posted")

    def test_day_number_and_past_texts(self):
        self.assertEqual(db.next_day_number(self.conn), 1)
        self.assertEqual(db.past_texts(self.conn), [])
        a = db.add_post(self.conn, "first", "p", status="posted")
        db.add_post(self.conn, "draft only", "p")
        b = db.add_post(self.conn, "second", "p")
        db.set_status(self.conn, b, "posted")
        self.assertEqual(db.next_day_number(self.conn), 3)
        self.assertEqual(db.past_texts(self.conn), ["first", "second"])
        self.assertLess(a, b)


if __name__ == "__main__":
    unittest.main()
