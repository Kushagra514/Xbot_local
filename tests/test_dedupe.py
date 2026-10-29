import unittest

from xbot.dedupe import is_duplicate, similarity


class TestDedupe(unittest.TestCase):
    def test_identical(self):
        self.assertEqual(similarity("Softmax turns logits", "softmax TURNS logits!"), 1.0)

    def test_disjoint(self):
        self.assertEqual(similarity("alpha beta", "gamma delta"), 0.0)

    def test_partial(self):
        self.assertAlmostEqual(similarity("a b c d", "c d e f"), 2 / 6)

    def test_empty(self):
        self.assertEqual(similarity("", ""), 0.0)
        self.assertEqual(similarity("", "abc"), 0.0)

    def test_punctuation_ignored(self):
        self.assertEqual(similarity("kv-cache, attention.", "kv cache attention"), 1.0)

    def test_is_duplicate(self):
        past = ["attention is all you need", "softmax turns logits into probabilities"]
        self.assertTrue(is_duplicate("Softmax turns logits into probabilities", past))
        self.assertFalse(is_duplicate("residual connections ease optimization", past))
        self.assertFalse(is_duplicate("anything", []))

    def test_threshold(self):
        past = ["a b c d"]
        self.assertTrue(is_duplicate("c d e f", past, threshold=0.33))
        self.assertFalse(is_duplicate("c d e f", past, threshold=0.34))


if __name__ == "__main__":
    unittest.main()
