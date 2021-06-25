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
    # fix bad inputs
    if max_colors > 20:
        max_colors = 20
    if max_colors <= 0:
        max_colors = 8
    if sensitivity > 250:
        sensitivity = 250
    if sensitivity < 0:
        sensitivity = 75

    # reduce all found colors using supplied sensitivity
    sampled_colors = []
    skipped = set()
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
        for found_color in sampled_colors:
            distance = color_distance(color, found_color)
            if distance <= sensitivity:
                skipped.add(color)
                break
        # if color wasn't too close to any appended colors keep it
        if color not in skipped:
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


def draw_swatches(colors: list, size: int = 200, cols: int = 4) -> object:
    """
    Generate a PIL Image object of color swatches.

    :param colors: a list of RGB color tuples (or lists)
    :param size: width in pixels of each color swatch (min=150, max=500)
    :param cols: number of swatches per row
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
    if total < cols:
        cols = total
    if total % cols == 0:
        rows = total // cols
    else:
        rows = (total // cols) + 1
    width = cols * size
    height = rows * size

    # create a new image and setup drawing object and font
    image = Image.new("RGB", (width, height), (255, 255, 255))
    d = ImageDraw.Draw(image)
    font = set_font("Arial Bold.ttf", size // 6)

    # iterate through all colors to create swatches
    for i, color in enumerate(colors):
        # if RGB values were provide in list, convert to tuple
        if type(color) == list:
            color = tuple(color)

        # calculate the swatch position and draw
        p1 = ((i % cols) * size, (i // cols) * size)
        p2 = (p1[0] + size, p1[1] + size)
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
