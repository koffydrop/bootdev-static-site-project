import unittest

import md.block as b


class TestBlock(unittest.TestCase):
    def test_markdown_to_blocks(self):
        md = """
This is **bolded** paragraph

This is another paragraph with _italic_ text and `code` here
This is the same paragraph on a new line

- This is a list
- with items
"""
        blocks = b.markdown_to_blocks(md)
        self.assertEqual(
            blocks,
            [
                "This is **bolded** paragraph",
                "This is another paragraph with _italic_ text and `code` here\nThis is the same paragraph on a new line",
                "- This is a list\n- with items",
            ],
        )

    def test_markdown_to_blocks_excess_newlines(self):
        md = """
This is **bolded** paragraph





This is another paragraph with _italic_ text and `code` here
This is the same paragraph on a new line



- This is a list
- with items
"""
        blocks = b.markdown_to_blocks(md)
        self.assertEqual(
            blocks,
            [
                "This is **bolded** paragraph",
                "This is another paragraph with _italic_ text and `code` here\nThis is the same paragraph on a new line",
                "- This is a list\n- with items",
            ],
        )

    def test_block_to_heading(self):
        blocks = [
            "not a heading",
            "# A heading",
            "## Another",
            "### Three",
            "#### Four",
            "##### Now number five",
            "###### I never wanna hear you say",
            "####### im just a paragraph",
        ]
        result = list(map(b.block_to_block_type, blocks))
        expect = [
            b.BlockType.PARAGRAPH,
            b.BlockType.HEADING,
            b.BlockType.HEADING,
            b.BlockType.HEADING,
            b.BlockType.HEADING,
            b.BlockType.HEADING,
            b.BlockType.HEADING,
            b.BlockType.PARAGRAPH,
        ]
        self.assertListEqual(result, expect)

    def test_block_to_code(self):
        block = """```rust
fn main() {
    println!("Hi there");
}
```"""
        self.assertEqual(b.block_to_block_type(block), b.BlockType.CODE)

    def test_block_to_quote(self):
        block = """> something really smart
> said by someone really smart"""
        self.assertEqual(b.block_to_block_type(block), b.BlockType.QUOTE)

    def test_block_to_unordered_list(self):
        block = """- an item
- another
- and another"""
        self.assertEqual(b.block_to_block_type(block), b.BlockType.UNORDERED_LIST)

    def test_block_to_ordered_list(self):
        block = """1. one
2. two
3. three
4. four"""
        self.assertEqual(b.block_to_block_type(block), b.BlockType.ORDERED_LIST)
