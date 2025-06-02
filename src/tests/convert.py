import unittest

from md.convert import markdown_to_html_node


class TestConvert(unittest.TestCase):
    def test_paragraphs(self):
        md = """
This is **bolded** paragraph
text in a p
tag here

This is another paragraph with _italic_ text and `code` here

"""
        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div><p>This is <b>bolded</b> paragraph text in a p tag here</p><p>This is another paragraph with <i>italic</i> text and <code>code</code> here</p></div>",
        )

    def test_codeblock(self):
        md = """
```
This is text that _should_ remain
the **same** even with inline stuff
```
"""

        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div><pre><code>This is text that _should_ remain\nthe **same** even with inline stuff\n</code></pre></div>",
        )

    def test_all(self):
        md = """
# h1

###### h6

paragraph with **bold** and _italics_
and [link](https://www.boot.dev) and ![image](https://www.boot.dev)

> a blockquote
> by someone probably

- unordered
- list

1. ordered
2. list
3. item

```
print("hello")
```
"""
        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            '<div><h1>h1</h1><h6>h6</h6><p>paragraph with <b>bold</b> and <i>italics</i> and <a href="https://www.boot.dev">link</a> and <img src="https://www.boot.dev" alt="image"></img></p><blockquote>a blockquote by someone probably</blockquote><ul><li>unordered</li><li>list</li></ul><ol><li>ordered</li><li>list</li><li>item</li></ol><pre><code>print("hello")\n</code></pre></div>',
        )
