from enum import Enum


class BlockType(Enum):
    PARAGRAPH = "paragraph"
    HEADING = "heading"
    CODE = "code"
    QUOTE = "quote"
    UNORDERED_LIST = "unordered_list"
    ORDERED_LIST = "ordered_list"


def markdown_to_blocks(md: str) -> list[str]:
    blocks = list(
        filter(
            lambda b: not any(b == s for s in ["\n", ""]),
            map(str.strip, md.split("\n\n")),
        )
    )
    return blocks


def block_to_block_type(block: str) -> BlockType:
    lines = block.split("\n")
    if any(block.startswith(h) for h in ["#" * i + " " for i in range(1, 7)]):
        return BlockType.HEADING
    if block.startswith("```") and block.endswith("```"):
        return BlockType.CODE
    if all(line.startswith(">") for line in lines):
        return BlockType.QUOTE
    if all(line.startswith("- ") for line in lines):
        return BlockType.UNORDERED_LIST
    if block.startswith("1.") and all(
        lines[i].startswith(str(i + 1)) for i in range(len(lines))
    ):
        return BlockType.ORDERED_LIST
    return BlockType.PARAGRAPH
