import unittest

from xbot.compose import compose_url


class TestCompose(unittest.TestCase):
    def test_encoding(self):
        self.assertEqual(
            compose_url("Day 1/100: hi & bye"),
            "https://x.com/intent/post?text=Day%201%2F100%3A%20hi%20%26%20bye",
        )

    def test_unicode(self):
        self.assertEqual(compose_url("ok 🙂"), "https://x.com/intent/post?text=ok%20%F0%9F%99%82")

    def test_empty(self):
        for bad in ("", "  \n"):
            with self.assertRaises(ValueError):
                compose_url(bad)

    def test_length(self):
        compose_url("a" * 280)
        with self.assertRaises(ValueError):
            compose_url("a" * 281)


if __name__ == "__main__":
    unittest.main()
