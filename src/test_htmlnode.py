import unittest
from htmlnode import HTMLNode


class TestHTMLNode(unittest.TestCase):
    def test_props_to_html(self):
        node = HTMLNode(
            "p", "some text", None, {"href": "https://boot.dev", "id": "my-link"}
        )
        expected = ' href="https://boot.dev" id="my-link"'

        self.assertEqual(expected, node.props_to_html())

    def test_repr(self):
        node = HTMLNode("p", "text")
        with_props = HTMLNode("a", None, None, {"id": "an-id"})
        expected = """HTMLNode(
            tag=p,
            value=text,
            children=None,
            props=
        )
        """
        expected_props = """HTMLNode(
            tag=a,
            value=None,
            children=None,
            props= id="an-id"
        )
        """
        self.assertEqual(f"{node}", expected)
        self.assertEqual(f"{with_props}", expected_props)

    def test_empty(self):
        node = HTMLNode()

        for item in node.__dict__.values():
            self.assertIsNone(item)


if __name__ == "__main__":
    unittest.main()
