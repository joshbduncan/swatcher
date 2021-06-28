import pytest

from swatcher import palette


COLORS = [
    (255, 203, 156),
    (218, 227, 226),
    (81, 63, 59),
    (157, 163, 163),
    (162, 166, 255),
    (255, 96, 93),
    (158, 107, 90),
    (107, 219, 255),
]


def test_01():  # image size with 8 swatches
    img = palette.draw_swatches(COLORS)
    assert img.size == (800, 400)


def test_02():  # image size with 16 swatches
    img = palette.draw_swatches(colors=COLORS * 2)
    assert img.size == (800, 800)


def test_03():  # image size with 100 px swatcher
    img = palette.draw_swatches(colors=COLORS, size=100)
    assert img.size == (600, 300)


def test_04():  # image size with less colors than cols
    img = palette.draw_swatches(COLORS[:2])
    assert img.size == (400, 200)
