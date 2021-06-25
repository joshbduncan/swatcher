import pytest

from PIL import Image, ImageDraw, ImageFilter
from swatcher import image


def test_01():  # one centered pixel
    img = Image.new("RGB", (1000, 1000), (255, 255, 255))
    d = ImageDraw.Draw(img)
    d.point((500, 500), (0, 0, 0))
    trimmed = image.trim_excess(img)
    assert trimmed.size == (1, 1)


def test_02():  # two inset pizels (top-left, bottom-right)
    img = Image.new("RGB", (1000, 1000), (255, 255, 255))
    d = ImageDraw.Draw(img)
    d.point(((10, 10), (990, 990)), (0, 0, 0))
    trimmed = image.trim_excess(img)
    assert trimmed.size == (981, 981)


def test_03():  # transparent circle centered
    img = Image.new("RGBA", (1000, 1000))
    d = ImageDraw.Draw(img)
    d.ellipse((400, 400, 600, 600), (255, 128, 0))
    trimmed = image.process_image(img)
    assert trimmed.size == (201, 201)


def test_04():  # transparent image two objects over 500 px
    img = Image.new("RGBA", (1000, 1000))
    d = ImageDraw.Draw(img)
    d.ellipse((100, 100, 200, 200), (0, 0, 0))
    d.ellipse((500, 500, 700, 700), (255, 128, 0))
    trimmed = image.process_image(img)
    assert trimmed.size == (500, 500)


def test_05():  # aliased pixels on solid background
    canvas_w, canvas_h = 1000, 800
    shape_w, shape_h = 600, 286
    img = Image.new("RGB", (canvas_w, canvas_h), (255, 255, 255))
    d = ImageDraw.Draw(img)
    p1 = ((canvas_w // 2) - (shape_w // 2), (canvas_h // 2) - (shape_h // 2))
    p2 = (p1[0] + shape_w, p1[1] + shape_h)
    d.ellipse(xy=(p1, p2), fill=(255, 0, 255))
    for _ in range(10):
        img = img.filter(ImageFilter.BLUR)
    aliased = image.process_image(img)
    assert aliased.size == (500, 250)


def test_06():  # aliased pixels on transparent background
    canvas_w, canvas_h = 1000, 800
    shape_w, shape_h = 600, 286
    img = Image.new("RGBA", (canvas_w, canvas_h), (0, 0, 0, 0))
    d = ImageDraw.Draw(img)
    p1 = ((canvas_w // 2) - (shape_w // 2), (canvas_h // 2) - (shape_h // 2))
    p2 = (p1[0] + shape_w, p1[1] + shape_h)
    d.ellipse(xy=(p1, p2), fill=(255, 0, 255))
    for _ in range(10):
        img = img.filter(ImageFilter.BLUR)
    aliased = image.process_image(img)
    assert aliased.size == (500, 250)


def test_07():  # image has no pixels
    with pytest.raises(ValueError):
        img = Image.new(size=(2, 0), mode="RGBA")
        img = image.process_image(img)


def test_08():  # small image
    img = Image.new(size=(50, 50), mode="RGBA")
    img = image.process_image(img)
    assert img.size == (50, 50)
