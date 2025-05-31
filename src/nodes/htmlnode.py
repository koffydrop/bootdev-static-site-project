from typing import Optional


class HTMLNode:
    def __init__(
        self,
        tag: Optional[str] = None,
        value: Optional[str] = None,
        children: Optional[list] = None,
        props: Optional[dict] = None,
    ):
        self.tag = tag
        self.value = value
        self.children = children
        self.props = props

    def to_html(self):
        raise NotImplementedError

    def props_to_html(self):
        if self.props is None:
            return ""
        else:
            return "".join(
                map(lambda props: f' {props[0]}="{props[1]}"', self.props.items())
            )

    def __repr__(self):
        return f"""HTMLNode(
    tag={self.tag},
    value={self.value},
    children={self.children},
    props={self.props_to_html()}
)
"""
