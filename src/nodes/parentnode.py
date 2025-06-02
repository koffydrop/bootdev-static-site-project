from typing import Optional, Sequence

from nodes.htmlnode import HTMLNode


class ParentNode(HTMLNode):
    def __init__(
        self, tag: str, children: Sequence[HTMLNode], props: Optional[dict] = None
    ):
        super().__init__(tag, children=children, props=props)

    def to_html(self) -> str:
        if self.tag is None:
            raise ValueError("ParentNode must have a tag")
        if self.children is None:
            raise ValueError("ParentNode must have children")

        rendered = [f"<{self.tag}{self.props_to_html()}>"]

        for child in self.children:
            rendered.append(child.to_html())

        rendered.append(f"</{self.tag}>")

        return "".join(rendered)
