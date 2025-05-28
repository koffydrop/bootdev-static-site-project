def markdown_to_blocks(md: str) -> list[str]:
    blocks = list(
        filter(
            lambda b: not any(b == s for s in ["\n", ""]),
            map(str.strip, md.split("\n\n")),
        )
    )
    return blocks
