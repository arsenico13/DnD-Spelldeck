from pathlib import Path


def write_text_file(path, content):
    Path(path).write_text(content)

