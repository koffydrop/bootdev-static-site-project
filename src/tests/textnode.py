import unittest

from nodes.textnode import TextNode, TextType


class TestTextNode(unittest.TestCase):
    def test_eq(self):
        node = TextNode("some text", TextType.TEXT)
        other = TextNode("some text", TextType.TEXT)

        self.assertEqual(node, other)

    def test_ne(self):
        node = TextNode("some text", TextType.ITALIC)
        with_url = TextNode("some text", TextType.ITALIC, "https://www.boot.dev")

        self.assertNotEqual(node, with_url)

    def test_invalid_type(self):
        with self.assertRaises(AttributeError) as res:
            TextNode("", TextType.INVALID)

        self.assertIsInstance(res.exception, AttributeError)


if __name__ == "__main__":
    unittest.main()
