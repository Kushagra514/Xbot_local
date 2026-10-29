import unittest
import os
import tempfile
from bot import knowledge_reader


class TestKnowledgeReader(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.mkdtemp()

    def _write(self, name, text):
        p = os.path.join(self.tmp, name)
        with open(p, "w", encoding="utf-8") as f:
            f.write(text)
        return p

    def test_reads_learnings(self):
        self._write("2026-10-20-softmax.md", "Pillar: Day N/100\n# Softmax\n\nturns logits into probabilities.\n")
        self._write("2026-10-21-lora.md", "# LoRA\n\nrank matters.\n")
        learnings = knowledge_reader.read_knowledge(self.tmp)
        self.assertEqual(len(learnings), 2)
        self.assertEqual(learnings[0].title, "Softmax")
        self.assertEqual(learnings[0].pillar, "Day N/100")
        self.assertIn("turns logits", learnings[0].body)
        self.assertEqual(learnings[1].title, "LoRA")
        self.assertEqual(learnings[1].pillar, "general")

    def test_skips_readme(self):
        self._write("README.md", "# ignore me\n")
        self._write("a.md", "# Real\n\nbody\n")
        learnings = knowledge_reader.read_knowledge(self.tmp)
        self.assertEqual([l.title for l in learnings], ["Real"])

    def test_missing_dir_returns_empty(self):
        self.assertEqual(knowledge_reader.read_knowledge("/nonexistent-dir-xyz"), [])


if __name__ == "__main__":
    unittest.main()
