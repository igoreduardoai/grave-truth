"""WCAG contrast math over rendered colors.

A gradient or other background image is not a resolved color. axe-core
reports that case as incomplete, and this module does not treat it as a pass.
"""

from __future__ import annotations

import re


def _channel(value: float) -> float:
    value = value / 255
    if value <= 0.04045:
        return value / 12.92
    return ((value + 0.055) / 1.055) ** 2.4


def _luminance(rgb: tuple[int, int, int]) -> float:
    red, green, blue = (_channel(part) for part in rgb)
    return 0.2126 * red + 0.7152 * green + 0.0722 * blue


def contrast_ratio(foreground: tuple[int, int, int], background: tuple[int, int, int]) -> float:
    lighter = max(_luminance(foreground), _luminance(background))
    darker = min(_luminance(foreground), _luminance(background))
    return (lighter + 0.05) / (darker + 0.05)


def parse_rgb(text: str) -> tuple[int, int, int] | None:
    raw = text.strip()
    if not raw.startswith("rgb"):
        return None
    numbers = []
    current = ""
    for char in raw:
        if char.isdigit():
            current += char
        elif current:
            numbers.append(int(current))
            current = ""
    if current:
        numbers.append(int(current))
    if len(numbers) < 3:
        return None
    return numbers[0], numbers[1], numbers[2]


def parse_css_color(text: str) -> tuple[int, int, int, float] | None:
    """Return red, green, blue, and alpha. Alpha is 1 when the color has none."""
    raw = text.strip()
    if not raw.lower().startswith("rgb"):
        return None
    parts = re.findall(r"[\d.]+", raw)
    if len(parts) < 3:
        return None
    red, green, blue = (int(float(part)) for part in parts[:3])
    alpha = float(parts[3]) if len(parts) > 3 else 1.0
    return red, green, blue, alpha


def _required_ratio(font_size: str, font_weight: str) -> float:
    size = float(str(font_size).strip().removesuffix("px"))
    weight_text = str(font_weight).strip().lower()
    if weight_text == "bold":
        weight = 700
    elif weight_text == "normal":
        weight = 400
    else:
        weight = int(float(weight_text))
    large = size >= 24 or (size >= 18.66 and weight >= 700)
    return 3.0 if large else 4.5


def _unresolved(reason: str) -> dict:
    return {
        "resolvable": False,
        "passes": False,
        "reason": reason,
        "ratio": None,
        "required": None,
    }


def assess_rendered_text(
    *,
    color: str,
    font_size: str,
    font_weight: str,
    opacity: str,
    layers: list[dict],
) -> dict:
    """Score one text node from computed CSS layers, nearest ancestor first.

    `layers` walks from the text element to the document element. A gradient
    or image on any ancestor means the color is not resolved. A solid opaque
    background is the color actually behind the text.
    """
    for layer in layers:
        image = (layer.get("backgroundImage") or "").strip()
        if image and image != "none":
            reason = "background gradient" if "gradient" in image else "background image"
            return _unresolved(reason)
        layer_opacity = float(layer.get("opacity") or 1)
        if layer_opacity < 1:
            return _unresolved("opacity")
    if float(opacity) < 1:
        return _unresolved("opacity")
    foreground = parse_css_color(color)
    if foreground is None or foreground[3] < 1:
        return _unresolved("text color")
    background = None
    for layer in layers:
        parsed = parse_css_color(layer.get("backgroundColor") or "")
        if parsed is None or parsed[3] == 0:
            continue
        if parsed[3] < 1:
            return _unresolved("translucent background")
        background = parsed[:3]
        break
    if background is None:
        return _unresolved("no opaque background")
    ratio = contrast_ratio(foreground[:3], background)
    required = _required_ratio(font_size, font_weight)
    return {
        "resolvable": True,
        "passes": ratio >= required,
        "reason": "rendered colors",
        "ratio": round(ratio, 2),
        "required": required,
        "foreground": foreground[:3],
        "background": background,
    }
