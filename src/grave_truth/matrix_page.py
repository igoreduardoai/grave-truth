"""HTML for the capability matrix. The words come from the markdown file."""

from __future__ import annotations

import html


def render_matrix_document(markdown: str) -> str:
    """Wrap the capability-matrix markdown in one local page."""
    body = _blocks(markdown)
    return f"""<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <title>Kiro capability matrix</title>
  <link rel="stylesheet" href="style.css">
</head>
<body>
  <a class="skip" href="#matrix">Skip to matrix</a>
  <main>
    <article id="matrix" class="matrix">
{body}
    </article>
  </main>
</body>
</html>
"""


def _blocks(markdown: str) -> str:
    lines = markdown.splitlines()
    parts: list[str] = []
    index = 0
    while index < len(lines):
        line = lines[index]
        if not line.strip():
            index += 1
            continue
        if line.startswith("#"):
            level = len(line) - len(line.lstrip("#"))
            level = min(max(level, 1), 3)
            text = line[level:].strip()
            parts.append(f"    <h{level}>{html.escape(text)}</h{level}>")
            index += 1
            continue
        if _is_table_start(lines, index):
            header = _cells(line)
            index += 2
            rows = []
            while index < len(lines) and lines[index].startswith("|"):
                rows.append(_cells(lines[index]))
                index += 1
            parts.append(_table(header, rows))
            continue
        if line.startswith("- "):
            items = []
            while index < len(lines) and lines[index].startswith("- "):
                items.append(f"      <li>{html.escape(lines[index][2:].strip())}</li>")
                index += 1
            parts.append("    <ul>\n" + "\n".join(items) + "\n    </ul>")
            continue
        paragraph = [line.strip()]
        index += 1
        while index < len(lines) and lines[index].strip() and not _starts_block(lines[index]):
            paragraph.append(lines[index].strip())
            index += 1
        parts.append(f"    <p>{html.escape(' '.join(paragraph))}</p>")
    return "\n".join(parts)


def _starts_block(line: str) -> bool:
    return line.startswith("#") or line.startswith("|") or line.startswith("- ")


def _is_table_start(lines: list[str], index: int) -> bool:
    if not lines[index].startswith("|") or index + 1 >= len(lines):
        return False
    separator = lines[index + 1]
    if not separator.startswith("|"):
        return False
    leftover = separator.replace("|", "").replace(":", "").replace("-", "").strip()
    return leftover == ""


def _cells(line: str) -> list[str]:
    parts = [part.strip() for part in line.strip().strip("|").split("|")]
    return parts


def _table(header: list[str], rows: list[list[str]]) -> str:
    head = "".join(f"<th>{html.escape(cell)}</th>" for cell in header)
    body = []
    for row in rows:
        cells = "".join(f"<td>{html.escape(cell)}</td>" for cell in row)
        body.append(f"      <tr>{cells}</tr>")
    return (
        "    <table>\n"
        f"      <thead><tr>{head}</tr></thead>\n"
        "      <tbody>\n"
        + "\n".join(body)
        + "\n      </tbody>\n"
        "    </table>"
    )
