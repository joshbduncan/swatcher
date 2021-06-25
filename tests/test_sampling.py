from PIL import Image, ImageDraw
from swatcher import color, palette


def test_01():  # sampled_colors from control image
    img = Image.new("RGB", (3, 1), (255, 255, 255))
    d = ImageDraw.Draw(img)
    d.point((0, 0), (255, 0, 0))
    d.point((1, 0), (0, 255, 0))
    d.point((2, 0), (0, 0, 255))
    image_colors = color.get_colors(img)
    sampled_colors = palette.sample(image_colors)
    assert sampled_colors == [(255, 0, 0), (0, 255, 0), (0, 0, 255)]


def test_02():  # sampled_colors from control image
    img = Image.new("RGB", (3, 1), (255, 255, 255))
    d = ImageDraw.Draw(img)
    d.point((0, 0), (0, 0, 255))
    d.point((1, 0), (0, 255, 0))
    d.point((2, 0), (255, 0, 0))
    image_colors = color.get_colors(img)
    sampled_colors = palette.sample(image_colors)
    assert sampled_colors == [(0, 0, 255), (0, 255, 0), (255, 0, 0)]


def test_03():  # sampled_colors from control image
    img = Image.new("RGB", (4, 1), (255, 255, 255))
    d = ImageDraw.Draw(img)
    d.point(((0, 0), (1, 0)), (255, 0, 0))
    d.point((2, 0), (0, 255, 0))
    d.point((3, 0), (0, 0, 255))
    image_colors = color.get_colors(img)
    sampled_colors = palette.sample(image_colors)
    assert sampled_colors == [(255, 0, 0), (0, 255, 0), (0, 0, 255)]


def test_04():  # sampled_colors from control image
    img = Image.new("RGB", (4, 1), (255, 255, 255))
    d = ImageDraw.Draw(img)
    d.point((0, 0), (255, 0, 0))
    d.point(((1, 0), (2, 0)), (0, 255, 0))
    d.point((3, 0), (0, 0, 255))
    image_colors = color.get_colors(img)
    sampled_colors = palette.sample(image_colors)
    assert sampled_colors == [(0, 255, 0), (255, 0, 0), (0, 0, 255)]


def test_05():  # sampled_colors from control image
    img = Image.new("RGB", (4, 1), (255, 255, 255))
    d = ImageDraw.Draw(img)
    d.point((0, 0), (255, 0, 0))
    d.point((1, 0), (0, 255, 0))
    d.point(((2, 0), (3, 0)), (0, 0, 255))
    image_colors = color.get_colors(img)
    sampled_colors = palette.sample(image_colors)
    assert sampled_colors == [(0, 0, 255), (255, 0, 0), (0, 255, 0)]


def test_06():  # sampled_colors from control image
    img = Image.new("RGB", (4, 4), (255, 255, 255))
    d = ImageDraw.Draw(img)
    d.point(((0, 0), (1, 0), (0, 1), (1, 1)), (255, 0, 0))
    d.point(((2, 0), (3, 0), (2, 1), (3, 1)), (0, 255, 0))
    d.point(((0, 2), (1, 2), (0, 3), (1, 3)), (0, 0, 255))
    image_colors = color.get_colors(img)
    sampled_colors = palette.sample(image_colors)
    assert sampled_colors == [
        (255, 0, 0),
        (0, 255, 0),
        (0, 0, 255),
        (255, 255, 255),
    ]


def test_07():  # sample function on sample list
    assert palette.sample([(0, 0, 0), (128, 128, 128)]) == [
        (0, 0, 0),
        (128, 128, 128),
    ]


def test_08():  # sample function on sample list with increased sensitivity
    assert palette.sample([(0, 0, 0), (128, 128, 128)], sensitivity=250) == [(0, 0, 0)]


def test_09():  # sample function on sample list with reduced max_colors
    colors = [(255, 0, 0), (0, 255, 0), (0, 0, 255), (255, 255, 0), (255, 0, 255)]
    assert palette.sample(colors, max_colors=3) == [
        (255, 0, 0),
        (0, 255, 0),
        (0, 0, 255),
    ]
