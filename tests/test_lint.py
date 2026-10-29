import unittest

from xbot.lint import lint_post


class TestLint(unittest.TestCase):
    def test_clean(self):
        self.assertEqual(lint_post("Day 4/100: softmax turns logits into probabilities."), [])

    def test_empty(self):
        self.assertEqual(lint_post(""), ["empty"])
        self.assertEqual(lint_post("   \n"), ["empty"])

    def test_too_long(self):
        self.assertEqual(lint_post("a" * 280), [])
        self.assertEqual(lint_post("a" * 281), ["too_long"])

    def test_link(self):
        self.assertEqual(lint_post("read https://arxiv.org/abs/1"), ["has_link"])
        self.assertEqual(lint_post("see www.example.com"), ["has_link"])

    def test_banned_phrase(self):
        self.assertEqual(lint_post("This is a Game-Changer"), ["banned_phrase"])
        self.assertEqual(lint_post("Let us DELVE into attention"), ["banned_phrase"])
        self.assertEqual(lint_post("shipping today 🚀"), ["banned_phrase"])

    def test_hashtags(self):
        self.assertEqual(lint_post("#ml #ai learning"), [])
        self.assertEqual(lint_post("#ml #ai #llm learning"), ["too_many_hashtags"])

    def test_multiple_in_order_no_duplicates(self):
        text = "unlock unlock https://x.com " + "a" * 300 + " #a #b #c"
        self.assertEqual(lint_post(text), ["too_long", "has_link", "banned_phrase", "too_many_hashtags"])


if __name__ == "__main__":
    unittest.main()
