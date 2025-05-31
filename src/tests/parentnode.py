import unittest

from nodes.leafnode import LeafNode
from nodes.parentnode import ParentNode


class TestParentNode(unittest.TestCase):
    def test_to_html_with_children(self):
        child_node = LeafNode("span", "child")
        parent_node = ParentNode("div", [child_node])
        self.assertEqual(parent_node.to_html(), "<div><span>child</span></div>")

    def test_to_html_with_grandchildren(self):
        grandchild_node = LeafNode("b", "grandchild")
        child_node = ParentNode("span", [grandchild_node])
        parent_node = ParentNode("div", [child_node])
        self.assertEqual(
            parent_node.to_html(),
            "<div><span><b>grandchild</b></span></div>",
        )

    def test_to_html_with_props(self):
        child = LeafNode("p", "firstborn")
        parent = ParentNode("div", [child], {"id": "1", "class": "sacrifice"})

        self.assertEqual(
            parent.to_html(), '<div id="1" class="sacrifice"><p>firstborn</p></div>'
        )

    def test_grandchild_with_props(self):
        grandchild = LeafNode(None, "so cool", {"cool": "true"})
        child = ParentNode("span", [grandchild], {"id": "pipebomb"})
        node = ParentNode("div", [child], {"surprised": "sure is"})

        self.assertEqual(
            node.to_html(),
            '<div surprised="sure is"><span id="pipebomb">so cool</span></div>',
        )

    def test_to_html_siblings_nested_and_props(self):
        see = LeafNode("p", "lemme see what you have?")
        knife = LeafNode("i", "a knife!")
        bold = LeafNode("b", "NO!")
        no = ParentNode("i", children=[bold])
        node = ParentNode("div", [see, knife, no], {"silly": "yes"})

        self.assertEqual(
            node.to_html(),
            '<div silly="yes"><p>lemme see what you have?</p><i>a knife!</i><i><b>NO!</b></i></div>',
        )
