from math import sqrt, isqrt
from PIL import Image, ImageDraw, ImageFont
from swatcher.color import color_distance, normalize_rgb_values, rgb_2_hex, rgb_2_luma


def sample(colors: list, max_colors: int = 8, sensitivity: int = 75) -> list:
    """
    Sample most common colors from a PIL Image object.

    :param colors: list of RGB color tuples eg. [(0, 0, 0), (255, 255, 255)]
    :param max_colors: maximum number of colors to return
    :param sensitivity: how perceptively different (Euclidean Distance) a color
                    must be from others to be included in the sampled palette.
    :returns: list of most common colors in RGB tuples (255, 255, 255)
    """

    # reduce all found colors using supplied sensitivity
    sampled_colors = []
    for color in colors:
        # if max_color limit reached stop looking
        if len(sampled_colors) == max_colors:
            break
        # clean-up any slight color differences in PIL sampling
        color = normalize_rgb_values(color)
        # if most common color (first color) append it
        if sampled_colors == []:
            sampled_colors.append(color)
            continue
        # calculate Euclidean distance for a color against colors
        # already appended to determine if it shoule be ignored
        if not any(
            color_distance(color, found) <= sensitivity for found in sampled_colors
        ):
            sampled_colors.append(color)

    return sampled_colors


def set_font(fontface: str, size: int) -> object:
    """
    Setup PIL ImageFont objects in the given font and for use when drawing.

    :param fontface: a filename or file-like object containing a
                     TrueType font. If the file is not found in this
                     filename, the loader may also search in other
                     directories, such as the fonts/ directory on Windows
                     or /Library/Fonts/, /System/Library/Fonts/
                     and ~/Library/Fonts/ on macOS.
    :param size: the requested font size in points
    :returns: PIL ImageFont object
    """
    try:
        font = ImageFont.truetype(fontface, size)
    except OSError:
        print(f"Error! {fontface} font could not be found. Substituting default.")
        font = ImageFont.load_default()
    return font


def perfect_square(i: int) -> bool:
    """Determine is a number is a perfect square"""
    return i == isqrt(i) ** 2


def cols_and_rows(i: int) -> tuple:
    """Calculate the best layout for drawing all swatches."""
    if perfect_square(i):
        cols = rows = int(sqrt(i))
    else:
        if i <= 5:
            div = 1
        elif i <= 10:
            div = 2
        else:
            div = 4
        # determine columns needed
        if i <= 5 or i % 2 == 0:
            cols = i // div
        else:
            cols = (i + 1) // div
        # determine rows needed
        if i % cols == 0:
            rows = i // cols
        else:
            rows = (i // cols) + 1
    return (cols, rows)


def draw_swatches(colors: list, size: int = 200) -> object:
    """
    Generate a PIL Image object of color swatches.

    :param colors: a list of RGB color tuples (or lists)
    :param size: width in pixels of each color swatch (min=150, max=500)
    :returns: PIL Image object
    """

    # if requested size is odd add +1 so no half pixels
    if size % 2 != 0:
        size += 1
    # adjust size if out of bounds
    if size < 150:
        size = 150
    elif size > 500:
        size = 500

    # calculate the required rows, columns, and final image size
    total = len(colors)
    cols, rows = cols_and_rows(total)
    width = cols * size
    height = rows * size

    # create a new image and setup drawing object and font
    image = Image.new("RGBA", (width, height), (255, 255, 255, 0))
    d = ImageDraw.Draw(image)
    font = set_font("Arial Bold.ttf", size // 6)

    # iterate through all colors to create swatches
    for i, color in enumerate(colors):
        # if RGB values were provide in list, convert to tuple
        if type(color) == list:
            color = tuple(color)

        # calculate the swatch position and draw
        p1 = ((i % cols) * size, (i // cols) * size)
        p2 = (p1[0] + size - 1, p1[1] + size - 1)
        d.rectangle(xy=(p1, p2), fill=color)

        # convert rgb values to hex code
        # Determine the correct overlay text color
        # based on the brightness of the color swatch
        hex = rgb_2_hex(color)
        if rgb_2_luma(color) >= 0.50:
            text_fill = "black"
        else:
            text_fill = "white"
        # calculate the text center position and insert
        cp = [((p1[0] + p2[0]) // 2), ((p1[1] + p2[1]) // 2)]
        d.text(xy=cp, text=hex, fill=text_fill, anchor="mm", font=font)

    return image
