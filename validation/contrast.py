"""WCAG contrast math and a note when axe cannot see a gradient background."""

from __future__ import annotations


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
