from htmlnode import HTMLNode


class LeafNode(HTMLNode):
    def __init__(self, tag: str | None, value: str, props: dict | None = None):
        super().__init__(tag, value, None, props)

    def to_html(self) -> str:
        if self.value is None:
            raise ValueError("LeafNode must have a value")
        if self.tag is None:
            return self.value

        return "".join(
            [f"<{self.tag}{self.props_to_html()}>", self.value, f"</{self.tag}>"]
        )
