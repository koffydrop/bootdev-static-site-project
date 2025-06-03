import re

import md.inline as inline
from md.block import markdown_to_blocks, block_to_block_type, BlockType
from nodes.htmlnode import HTMLNode
from nodes.leafnode import LeafNode
from nodes.parentnode import ParentNode


def text_to_children(text: str) -> list[LeafNode]:
    text = text.replace("\n", " ")
    text_nodes = inline.text_to_textnodes(text)
    return [inline.text_node_to_html_node(node) for node in text_nodes]


def markdown_to_html_node(md: str) -> ParentNode:
    blocks = markdown_to_blocks(md)
    final_nodes: list[HTMLNode] = []
    for block in blocks:
        type = block_to_block_type(block)
        match type:
            case BlockType.PARAGRAPH:
                final_nodes.append(ParentNode("p", text_to_children(block)))
            case BlockType.HEADING:
                count = block.count("#")
                block = block.lstrip("# ")
                final_nodes.append(ParentNode(f"h{count}", text_to_children(block)))
            case BlockType.QUOTE:
                block = "\n".join(map(lambda b: b.lstrip("> "), block.split("\n")))
                final_nodes.append(ParentNode("blockquote", text_to_children(block)))
            case BlockType.CODE:
                block = block.lstrip("```\n").rstrip("```")
                final_nodes.append(
                    ParentNode(
                        "pre",
                        [
                            inline.text_node_to_html_node(
                                inline.TextNode(block, inline.TextType.CODE)
                            )
                        ],
                    )
                )
            case BlockType.ORDERED_LIST:
                final_nodes.append(
                    ParentNode(
                        "ol",
                        list(
                            map(
                                lambda item: ParentNode(
                                    "li",
                                    text_to_children(re.sub(r"^\d+\.\s+", "", item)),
                                ),
                                block.split("\n"),
                            )
                        ),
                    )
                )
            case BlockType.UNORDERED_LIST:
                final_nodes.append(
                    ParentNode(
                        "ul",
                        list(
                            map(
                                lambda item: ParentNode(
                                    "li", text_to_children(re.sub(r"^-\s+", "", item))
                                ),
                                block.split("\n"),
                            )
                        ),
                    )
                )
    return ParentNode("div", final_nodes)


def extract_title(md: str) -> str:
    for line in md.split("\n"):
        if line.startswith("# "):
            return line.lstrip("#").strip()
    raise Exception(f"no header in {md}")
