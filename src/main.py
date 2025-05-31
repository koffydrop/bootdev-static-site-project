from nodes.textnode import TextNode, TextType


def main() -> None:
    node: TextNode = TextNode("this is text", TextType.TEXT)
    print(node)


if __name__ == "__main__":
    main()
