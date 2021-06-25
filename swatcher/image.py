from collections import Counter
from PIL import Image, ImageChops
from .color import normalize_rgb_values


def trim_excess(image: object) -> object:
    """
    Trim excess background pixels from around an image.

    :param image: PIL Image object
    :returns: PIL Image object
    """
    w, h = image.size

    # get RGB value for each corner of image
    corners = [
        normalize_rgb_values(image.getpixel((0, 0))),
        normalize_rgb_values(image.getpixel((w - 1, 0))),
        normalize_rgb_values(image.getpixel((0, h - 1))),
        normalize_rgb_values(image.getpixel((w - 1, h - 1))),
    ]
    # count how many times each value is present
    color_count = Counter([pixel for pixel in corners]).most_common()

    # use the top left pixel as a base case
    bg_pixel = image.getpixel((0, 0))

    # if four corners don't match
    if len(color_count) > 1:
        # and multiple corners don't have the same count
        if color_count[0][1] != color_count[1][1]:
            # set the comparison pixel to the most common value
            bg_pixel = color_count[0][0]
        else:
            # if two corners have the same count don't trim
            return image

    # compare the original image to the excess pixels
    comparison = Image.new("RGB", image.size, bg_pixel)
    diff = ImageChops.difference(image, comparison)
    bbox = diff.getbbox()
    # crop the image to the difference
    return image.crop(bbox)


def process_image(image: object, max_size: int = 500) -> object:
    """
    Flatten, Crop, and Scale the provided image.

    :param image: PIL Image object
    :param max_size: maximum size of the image for color sampling
    :returns: PIL Image object
    """
    image = image.convert("RGBA")
    # check to make sure image has pixels
    w, h = image.size
    if w == 0 or h == 0:
        raise ValueError("The provided image has no pixels.")

    # composite the image on a white background just in case it has transparency
    background = Image.new("RGBA", image.size, (255, 255, 255))
    composite = Image.alpha_composite(background, image)
    # convert composite image to RGB since we only need the RGB color values
    composite = composite.convert("RGB")
    # crop the image if extra surrounding background pixels are found
    composite = trim_excess(composite)
    # reduce the image down to `max_size` to speed up processing
    if composite.width > max_size or composite.height > max_size:
        new_size = (max_size, max_size)
        composite.thumbnail(new_size, resample=0)

    return composite
