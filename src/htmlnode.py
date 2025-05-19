class HTMLNode:
    def __init__(
        self,
        tag: str | None = None,
        value: str | None = None,
        children: list | None = None,
        props: dict | None = None,
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
            return "".join(map(lambda t: f' {t[0]}="{t[1]}"', self.props.items()))

    def __repr__(self):
        return f"""HTMLNode(
            tag={self.tag},
            value={self.value},
            children={self.children},
            props={self.props_to_html()}
        )
        """
