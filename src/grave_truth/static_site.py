"""Write the files a static host could serve later. This module does not deploy them."""

from __future__ import annotations

import shutil
from pathlib import Path

from grave_truth.artifact import build_artifact
from grave_truth.health import HEALTH_BODY
from grave_truth.matrix_page import render_matrix_document

_HAUNTED = Path(__file__).resolve().parents[2] / "demos" / "haunted"
_ASSETS = ("index.html", "app.js", "style.css")


def build(dest: Path) -> None:
    dest = Path(dest)
    dest.mkdir(parents=True, exist_ok=True)
    for name in _ASSETS:
        shutil.copyfile(_HAUNTED / name, dest / name)
    (dest / "health").write_bytes(HEALTH_BODY)
    (dest / "health.json").write_bytes(HEALTH_BODY)
    letter = build_artifact("eob")
    clauses = build_artifact("lease")
    (dest / letter["filename"]).write_text(letter["markdown"], encoding="utf-8")
    (dest / clauses["filename"]).write_text(clauses["markdown"], encoding="utf-8")
    (dest / "judge.html").write_text(_judge_page(letter["markdown"]), encoding="utf-8")
    matrix = Path(__file__).resolve().parents[2] / "docs" / "KIRO-CAPABILITY-MATRIX.md"
    (dest / "kiro.html").write_text(
        render_matrix_document(matrix.read_text(encoding="utf-8")),
        encoding="utf-8",
    )


def _judge_page(markdown: str) -> str:
    escaped = (
        markdown.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")
    )
    return f"""<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <title>Grave Truth — synthetic dispute letter</title>
  <link rel="stylesheet" href="style.css">
</head>
<body>
  <header class="hero" id="hero">
    <p class="eyebrow">Pre-rendered synthetic sample · no API key · live model unimplemented</p>
    <h1>A figure stays only when the document states it.</h1>
    <ol class="storyboard">
      <li><span class="step">Input.</span> The patient responsibility is $42.15.</li>
      <li><span class="step">Check.</span> The offline checker quotes that sentence, or it says not found.</li>
      <li><span class="step">Result.</span> The dispute letter is the file below. Each cited line names its span.</li>
    </ol>
    <p class="disclaimer">Research demo on synthetic text. Not a medical device and not legal advice. This file does not call a model.</p>
  </header>
  <main>
    <h2>Synthetic dispute letter</h2>
    <pre id="artifact">{escaped}</pre>
  </main>
</body>
</html>
"""
