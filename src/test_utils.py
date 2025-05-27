import unittest
from textnode import TextNode, TextType
import utils as u


class TestUtils(unittest.TestCase):
    def test_text(self):
        node = TextNode("This is a text node", TextType.TEXT)
        html_node = u.text_node_to_html_node(node)
        self.assertEqual(html_node.tag, None)
        self.assertEqual(html_node.value, "This is a text node")

    def test_to_link(self):
        node = TextNode("boots", TextType.LINK, "https://www.boot.dev")
        leaf = u.text_node_to_html_node(node)

        self.assertEqual(leaf.tag, "a")
        self.assertEqual(leaf.props["href"], "https://www.boot.dev")

    def test_to_image(self):
        node = TextNode(
            "sneaky snek",
            TextType.IMAGE,
            "https://ih1.redbubble.net/image.4179810400.4645/bg,f8f8f8-flat,750x,075,f-pad,750x1000,f8f8f8.jpg",
        )
        leaf = u.text_node_to_html_node(node)

        self.assertEqual(leaf.value, "")
        self.assertEqual(leaf.tag, "img")
        self.assertEqual(
            leaf.props["src"],
            "https://ih1.redbubble.net/image.4179810400.4645/bg,f8f8f8-flat,750x,075,f-pad,750x1000,f8f8f8.jpg",
        )
        self.assertEqual(leaf.props["alt"], "sneaky snek")

    def test_split_node(self):
        cases = [
            ([TextNode("some **bold** text", TextType.TEXT)], "**", TextType.BOLD),
            (
                [TextNode("some _italics_, and _a bit_ more", TextType.TEXT)],
                "_",
                TextType.ITALIC,
            ),
            ([TextNode("`a code block`", TextType.TEXT)], "`", TextType.CODE),
        ]

        bolds = u.split_nodes_delimiter(*cases[0])
        bolds_expect = [
            TextNode("some ", TextType.TEXT),
            TextNode("bold", TextType.BOLD),
            TextNode(" text", TextType.TEXT),
        ]
        italics = u.split_nodes_delimiter(*cases[1])
        italics_expect = [
            TextNode("some ", TextType.TEXT),
            TextNode("italics", TextType.ITALIC),
            TextNode(", and ", TextType.TEXT),
            TextNode("a bit", TextType.ITALIC),
            TextNode(" more", TextType.TEXT),
        ]
        codes = u.split_nodes_delimiter(*cases[2])
        codes_expect = [TextNode("a code block", TextType.CODE)]

        self.assertEqual(bolds, bolds_expect)
        self.assertEqual(italics, italics_expect)
        self.assertEqual(codes, codes_expect)

    def test_extract_image(self):
        text = "This is text with a ![rick roll](https://i.imgur.com/aKaOqIh.gif), ![obi wan](https://i.imgur.com/fJRm4Vk.jpeg), and a regular [link](https://www.boot.dev)"
        result = u.extract_markdown_images(text)

        self.assertListEqual(
            result,
            [
                ("rick roll", "https://i.imgur.com/aKaOqIh.gif"),
                ("obi wan", "https://i.imgur.com/fJRm4Vk.jpeg"),
            ],
        )

    def test_extract_link(self):
        text = "This is text with a link [to boot dev](https://www.boot.dev), [to youtube](https://www.youtube.com/@bootdotdev) and an ![image](https://i.imgur.com/aKaOqIh.gif)"
        result = u.extract_markdown_links(text)

        self.assertListEqual(
            result,
            [
                ("to boot dev", "https://www.boot.dev"),
                ("to youtube", "https://www.youtube.com/@bootdotdev"),
            ],
        )

    def test_split_images(self):
        node = TextNode(
            "This is text with an ![image](https://i.imgur.com/zjjcJKZ.png) and another ![second image](https://i.imgur.com/3elNhQu.png)",
            TextType.TEXT,
        )
        new_nodes = u.split_nodes_image([node])
        self.assertListEqual(
            [
                TextNode("This is text with an ", TextType.TEXT),
                TextNode("image", TextType.IMAGE, "https://i.imgur.com/zjjcJKZ.png"),
                TextNode(" and another ", TextType.TEXT),
                TextNode(
                    "second image", TextType.IMAGE, "https://i.imgur.com/3elNhQu.png"
                ),
            ],
            new_nodes,
        )

    def test_split_images_mixed_link(self):
        node = TextNode(
            "This is text with an ![image](https://i.imgur.com/zjjcJKZ.png) and another ![second image](https://i.imgur.com/3elNhQu.png) and a sneaky [link!](https://www.boot.dev)",
            TextType.TEXT,
        )
        new_nodes = u.split_nodes_image([node])
        self.assertListEqual(
            [
                TextNode("This is text with an ", TextType.TEXT),
                TextNode("image", TextType.IMAGE, "https://i.imgur.com/zjjcJKZ.png"),
                TextNode(" and another ", TextType.TEXT),
                TextNode(
                    "second image", TextType.IMAGE, "https://i.imgur.com/3elNhQu.png"
                ),
                TextNode(" and a sneaky [link!](https://www.boot.dev)", TextType.TEXT),
            ],
            new_nodes,
        )

    def test_split_links(self):
        node = TextNode(
            "This is text with a [link](https://i.imgur.com/zjjcJKZ.png) and another [second link](https://i.imgur.com/3elNhQu.png)",
            TextType.TEXT,
        )
        new_nodes = u.split_nodes_link([node])
        self.assertListEqual(
            [
                TextNode("This is text with a ", TextType.TEXT),
                TextNode("link", TextType.LINK, "https://i.imgur.com/zjjcJKZ.png"),
                TextNode(" and another ", TextType.TEXT),
                TextNode(
                    "second link", TextType.LINK, "https://i.imgur.com/3elNhQu.png"
                ),
            ],
            new_nodes,
        )

    def test_split_links_mixed_image(self):
        node = TextNode(
            "This is text with a [link](https://i.imgur.com/zjjcJKZ.png) and another [second link](https://i.imgur.com/3elNhQu.png) and a sneaky ![image](https://i.imgur.com/3elNhQu.png)!",
            TextType.TEXT,
        )
        new_nodes = u.split_nodes_link([node])
        self.assertListEqual(
            [
                TextNode("This is text with a ", TextType.TEXT),
                TextNode("link", TextType.LINK, "https://i.imgur.com/zjjcJKZ.png"),
                TextNode(" and another ", TextType.TEXT),
                TextNode(
                    "second link", TextType.LINK, "https://i.imgur.com/3elNhQu.png"
                ),
                TextNode(
                    " and a sneaky ![image](https://i.imgur.com/3elNhQu.png)!",
                    TextType.TEXT,
                ),
            ],
            new_nodes,
        )

    def test_split_images_many_nodes(self):
        node = TextNode(
            "![image](https://i.imgur.com/3elNhQu.png) right there", TextType.TEXT
        )
        node2 = TextNode(
            "an ![image](https://i.imgur.com/3elNhQu.png) and a [link](https://www.boot.dev)",
            TextType.TEXT,
        )

        new_nodes = u.split_nodes_image([node, node2])

        self.assertListEqual(
            [
                TextNode("image", TextType.IMAGE, "https://i.imgur.com/3elNhQu.png"),
                TextNode(" right there", TextType.TEXT),
                TextNode("an ", TextType.TEXT),
                TextNode("image", TextType.IMAGE, "https://i.imgur.com/3elNhQu.png"),
                TextNode(" and a [link](https://www.boot.dev)", TextType.TEXT),
            ],
            new_nodes,
        )

    def test_split_links_many_nodes(self):
        node = TextNode(
            "[link](https://i.imgur.com/3elNhQu.png) right there", TextType.TEXT
        )
        node2 = TextNode(
            "a [link](https://www.boot.dev) and an ![image](https://i.imgur.com/3elNhQu.png)",
            TextType.TEXT,
        )

        new_nodes = u.split_nodes_link([node, node2])

        self.assertListEqual(
            [
                TextNode("link", TextType.LINK, "https://i.imgur.com/3elNhQu.png"),
                TextNode(" right there", TextType.TEXT),
                TextNode("a ", TextType.TEXT),
                TextNode("link", TextType.LINK, "https://www.boot.dev"),
                TextNode(
                    " and an ![image](https://i.imgur.com/3elNhQu.png)", TextType.TEXT
                ),
            ],
            new_nodes,
        )

    def test_text_to_nodes(self):
        text = "This is **text** with an _italic_ word and a `code block` and an ![obi wan image](https://i.imgur.com/fJRm4Vk.jpeg) and a [link](https://boot.dev)"
        result = u.text_to_textnodes(text)
        expect = [
            TextNode("This is ", TextType.TEXT),
            TextNode("text", TextType.BOLD),
            TextNode(" with an ", TextType.TEXT),
            TextNode("italic", TextType.ITALIC),
            TextNode(" word and a ", TextType.TEXT),
            TextNode("code block", TextType.CODE),
            TextNode(" and an ", TextType.TEXT),
            TextNode(
                "obi wan image", TextType.IMAGE, "https://i.imgur.com/fJRm4Vk.jpeg"
            ),
            TextNode(" and a ", TextType.TEXT),
            TextNode("link", TextType.LINK, "https://boot.dev"),
        ]
        self.assertListEqual(result, expect)

    def test_text_to_multiple_nodes(self):
        text = "This is **text** with an _italic_ word and a `code block` and an ![obi wan image](https://i.imgur.com/fJRm4Vk.jpeg) and a [link](https://boot.dev) and again, This is **text** with an _italic_ word and a `code block` and an ![obi wan image](https://i.imgur.com/fJRm4Vk.jpeg) and a [link](https://boot.dev)"
        result = u.text_to_textnodes(text)
        expect = [
            TextNode("This is ", TextType.TEXT),
            TextNode("text", TextType.BOLD),
            TextNode(" with an ", TextType.TEXT),
            TextNode("italic", TextType.ITALIC),
            TextNode(" word and a ", TextType.TEXT),
            TextNode("code block", TextType.CODE),
            TextNode(" and an ", TextType.TEXT),
            TextNode(
                "obi wan image", TextType.IMAGE, "https://i.imgur.com/fJRm4Vk.jpeg"
            ),
            TextNode(" and a ", TextType.TEXT),
            TextNode("link", TextType.LINK, "https://boot.dev"),
            TextNode(" and again, This is ", TextType.TEXT),
            TextNode("text", TextType.BOLD),
            TextNode(" with an ", TextType.TEXT),
            TextNode("italic", TextType.ITALIC),
            TextNode(" word and a ", TextType.TEXT),
            TextNode("code block", TextType.CODE),
            TextNode(" and an ", TextType.TEXT),
            TextNode(
                "obi wan image", TextType.IMAGE, "https://i.imgur.com/fJRm4Vk.jpeg"
            ),
            TextNode(" and a ", TextType.TEXT),
            TextNode("link", TextType.LINK, "https://boot.dev"),
        ]
        self.assertListEqual(result, expect)

    def test_text_to_nodes_multiline(self):
        text = (
            "This is **text** with an _italic_ word\n"
            "and a `code block`\n"
            "and an ![obi wan image](https://i.imgur.com/fJRm4Vk.jpeg)\n"
            "and a [link](https://boot.dev)"
        )
        result = u.text_to_textnodes(text)
        expect = [
            TextNode("This is ", TextType.TEXT),
            TextNode("text", TextType.BOLD),
            TextNode(" with an ", TextType.TEXT),
            TextNode("italic", TextType.ITALIC),
            TextNode(" word\nand a ", TextType.TEXT),
            TextNode("code block", TextType.CODE),
            TextNode("\nand an ", TextType.TEXT),
            TextNode(
                "obi wan image", TextType.IMAGE, "https://i.imgur.com/fJRm4Vk.jpeg"
            ),
            TextNode("\nand a ", TextType.TEXT),
            TextNode("link", TextType.LINK, "https://boot.dev"),
        ]
        self.assertListEqual(result, expect)


if __name__ == "__main__":
    unittest.main()
