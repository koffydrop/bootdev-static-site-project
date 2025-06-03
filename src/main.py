import os
import shutil

from md.convert import markdown_to_html_node, extract_title


def main() -> None:
    static_to_public()
    generate_page("content/index.md", "template.html", "public/index.html")


def generate_page(from_path: str, template_path: str, dst_path: str) -> None:
    print(f"Generating page from {from_path} to {dst_path} using {template_path}")
    content = open(from_path).read()
    title = extract_title(content)
    template = open(template_path).read()
    html_content = markdown_to_html_node(content).to_html()
    doc = template.replace("{{ Title }}", title).replace("{{ Content }}", html_content)
    os.makedirs(os.path.dirname(dst_path), exist_ok=True)
    with open(dst_path, "x") as f:
        f.write(doc)


def static_to_public() -> None:
    src, dst = "static", "public"
    if not os.path.exists(src):
        raise FileNotFoundError(f"source folder {src} does not exist")
    copy_recursive(src, dst, True)


def copy_recursive(src: str, dst: str, first_call: bool = False) -> None:
    if first_call:
        print("Copying items...")
    if os.path.exists(dst):
        shutil.rmtree(dst)
    os.mkdir(dst)
    items = os.listdir(src)
    for item in items:
        src_item = os.path.join(src, item)
        dst_item = os.path.join(dst, item)
        if os.path.isfile(src_item):
            print(f"{src_item}  ->  {dst_item}")
            shutil.copy(src_item, dst)
        else:
            os.mkdir(dst_item)
            copy_recursive(src_item, dst_item)


if __name__ == "__main__":
    main()
