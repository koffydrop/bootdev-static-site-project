import unittest
from leafnode import LeafNode


class TestLeafNode(unittest.TestCase):
    def test_leaf_to_html_p(self):
        node = LeafNode("p", "Hello, world!")
        self.assertEqual(node.to_html(), "<p>Hello, world!</p>")

    def test_leaf_to_html_props(self):
        node = LeafNode("a", "some text", {"href": "https://www.boot.dev"})
        self.assertEqual(node.to_html(), '<a href="https://www.boot.dev">some text</a>')

    def test_leaf_without_tag(self):
        node = LeafNode(None, "a test of your reflexes")
        self.assertEqual(node.to_html(), "a test of your reflexes")


if __name__ == "__main__":
    unittest.main()
