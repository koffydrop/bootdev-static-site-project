from typing import Optional

from nodes.htmlnode import HTMLNode


class LeafNode(HTMLNode):
    def __init__(self, tag: Optional[str], value: str, props: Optional[dict] = None):
        super().__init__(tag, value, None, props)

    def to_html(self) -> str:
        if self.value is None:
            raise ValueError("LeafNode must have a value")
        if self.tag is None:
            return self.value

        return "".join(
            [f"<{self.tag}{self.props_to_html()}>", self.value, f"</{self.tag}>"]
        )
