from collections import Counter
from math import sqrt


def normalize_rgb_values(color: tuple) -> tuple:
    """
    Clean-up any slight color differences in PIL sampling.

    :param color: a tuple of RGB color values eg. (255, 255, 255)
    :returns: a tuple of RGB color values
    """
    return tuple([0 if val <= 3 else 255 if val >= 253 else val for val in color])


def rgb_2_luma(color: tuple) -> int:
    """
    Calculate the "brightness" of a color.

    ...and, yes I know this is a debated subject
    but this way works for just fine my purposes.

    :param color: a tuple of RGB color values eg. (255, 255, 255)
    :returns: luminance "brightness" value
    """
    r, g, b = color[0] / 255, color[1] / 255, color[2] / 255
    l = 0.33 * r + 0.5 * g + 0.16 * b
    return round(l, 2)


def sort_by_brightness(colors: list) -> list:
    """
    Sort of list of RGB colors values by their brightness.

    :param color: tuple of RGB values for color eg. (255, 255, 255)
    :returns: list of color value dictionaries
    """
    l = {color: rgb_2_luma(color) for color in colors}
    return sorted(l, key=l.get, reverse=True)


def rgb_2_hex(color: tuple) -> str:
    """
    Convert RGB color vales to Hex code (eg. #ffffff).

    :param color: tuple of RGB values for color eg. (255, 255, 255)
    :returns: color Hex code
    """
    r, g, b = color
    return f"#{r:02x}{g:02x}{b:02x}"


def rgb_2_cmyk(color: tuple) -> tuple:
    """
    Convert RGB color vales to CMYK color values.

    :param color: tuple of RGB values for color eg. (255, 255, 255)
    :returns: CMYK values eg. (C, M, Y, K)
    """

    # if RGB color is black return CMYK black
    if color == (0, 0, 0):
        return (0, 0, 0, 100)
    # convert the RGB values
    r, g, b = color
    k = 1 - max((r, g, b)) / 255
    c = int(((1 - (r / 255) - k) / (1 - k)) * 100)
    m = int(((1 - (g / 255) - k) / (1 - k)) * 100)
    y = int(((1 - (b / 255) - k) / (1 - k)) * 100)
    return (c, m, y, int(k * 100))


def color_2_dict(color: tuple) -> dict:
    """
    Convert tuple of RGB color vales to HEX and CMYK then
    combine into a dictionary in the following format.

    {"rgb": (0, 0, 0), "hex": "#000000", "cmyk": (0, 0, 0, 100)}

    :param color: tuple of RGB values for color eg. (255, 255, 255)
    :returns: RGB, HEX and CMYK values
    """
    rgb = color
    return {"rgb": rgb, "hex": rgb_2_hex(color), "cmyk": rgb_2_cmyk(color)}


def colors_2_dicts(colors: list) -> list:
    """
    Convert a list of RGB color vales to a list of
    dicts with RGB, HEX, and CMYK values.

    :param color: tuple of RGB values for color eg. (255, 255, 255)
    :returns: list of color value dictionaries
    """
    return [color_2_dict(color) for color in colors]


def color_distance(color1: tuple, color2: tuple) -> int:
    """
    Calculate the Euclidean distance between two colors.

    https://en.wikipedia.org/wiki/Color_difference

    :param color1: tuple of RGB color values eg. (255, 255, 255)
    :param color2: tuple of RGB color values
    :returns: Euclidean distance of two colors
    """
    r1, g1, b1 = color1
    r2, g2, b2 = color2
    return int(sqrt(((r2 - r1) ** 2) + ((g2 - g1) ** 2) + ((b2 - b1) ** 2)))


def get_colors(image: object) -> list:
    """
    Sample all pixels from an image and sort their RGB values by most common

    :param image: PIL Image object
    :returns: list of RGB tuples (255, 255, 255)
    """
    colors = Counter([pixel for pixel in image.getdata()])
    return [color for (color, _) in colors.most_common()]
