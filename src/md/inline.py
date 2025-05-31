import re
from functools import partial
from typing import Callable

from nodes.leafnode import LeafNode
from nodes.textnode import TextNode, TextType


IMAGE_REGEX = r"!\[([^\[\]]*)\]\(([^\(\)]*)\)"
LINK_REGEX = r"(?<!!)\[([^\[\]]*)\]\(([^\(\)]*)\)"


def split_nodes_delimiter(
    old_nodes: list[TextNode], delimiter: str, type: TextType
) -> list[TextNode]:
    new_nodes: list[TextNode] = []

    for node in old_nodes:
        split_text = node.text.split(delimiter)
        if len(split_text) <= 1:
            new_nodes.append(node)
            continue
        elif len(split_text) % 2 == 0:
            raise Exception(f"Unclosed delimiter in:\n{node.text}")

        for i in range(len(split_text)):
            current = split_text[i]
            if current == "":
                continue
            if i % 2 == 0:
                new_nodes.append(TextNode(current, node.type))
            else:
                new_nodes.append(TextNode(current, type))

    return new_nodes


split_bold = partial(split_nodes_delimiter, delimiter="**", type=TextType.BOLD)
split_italic = partial(split_nodes_delimiter, delimiter="_", type=TextType.ITALIC)
split_code = partial(split_nodes_delimiter, delimiter="`", type=TextType.CODE)


def extract_markdown_images(text: str) -> list[tuple[str, str]]:
    return re.findall(IMAGE_REGEX, text)


def extract_markdown_links(text: str) -> list[tuple[str, str]]:
    return re.findall(LINK_REGEX, text)


def split_nodes_pattern(
    pattern: str, extract_type: TextType, extractor: Callable
) -> Callable:
    def wrapper(old_nodes: list[TextNode]) -> list[TextNode]:
        new_nodes: list[TextNode] = []

        for node in old_nodes:
            if any(
                node.type == type
                for type in [TextType.LINK, TextType.IMAGE, TextType.CODE]
            ):
                new_nodes.append(node)
                continue

            extracted = extractor(node.text)

            if len(extracted) == 0:
                new_nodes.append(node)
                continue

            working_text = node.text

            for i in range(len(extracted)):
                alt, url = extracted[i]
                sep = pattern.format(alt, url)
                if i == len(extracted) - 1:
                    split_text = working_text.split(sep)
                    if split_text[0] != "":
                        new_nodes.append(TextNode(split_text[0], node.type))
                    new_nodes.append(TextNode(alt, extract_type, url))
                    for text in split_text[1:]:
                        if text != "":
                            new_nodes.append(TextNode(text, node.type))
                else:
                    text, working_text = working_text.split(sep, maxsplit=1)
                    if text != "":
                        new_nodes.append(TextNode(text, node.type))
                    new_nodes.append(TextNode(alt, extract_type, url))

        return new_nodes

    return wrapper


split_nodes_image = split_nodes_pattern(
    "![{}]({})", TextType.IMAGE, extract_markdown_images
)
split_nodes_link = split_nodes_pattern(
    "[{}]({})", TextType.LINK, extract_markdown_links
)


def text_node_to_html_node(text_node: TextNode) -> LeafNode:
    match text_node.type:
        case TextType.TEXT:
            return LeafNode(None, text_node.text)
        case TextType.BOLD:
            return LeafNode("b", text_node.text)
        case TextType.ITALIC:
            return LeafNode("i", text_node.text)
        case TextType.CODE:
            return LeafNode("code", text_node.text)
        case TextType.LINK:
            return LeafNode("a", text_node.text, {"href": text_node.url})
        case TextType.IMAGE:
            return LeafNode("img", "", {"src": text_node.url, "alt": text_node.text})
        case _:
            raise Exception("Invalid TextNode type")


def text_to_textnodes(text: str) -> list[TextNode]:
    nodes: list[TextNode] = [TextNode(text, TextType.TEXT)]
    ops: list[Callable] = [
        split_bold,
        split_code,
        split_italic,
        split_nodes_image,
        split_nodes_link,
    ]
    for fn in ops:
        nodes = fn(nodes)

    return nodes
