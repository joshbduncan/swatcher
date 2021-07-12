import os
import tempfile
import struct

from .color import rgb_2_hex


def format_ase_swatch(color: tuple) -> dict:
    """
    Create an Adobe ASE swatch dictionary in the following format.

    {
        'name': 'Swatch Name',
        'type': 'Process',
        'data': {
            'mode': 'RGB',
            'values': '[0, 0, 0]' # 0-1 channel value / 255
        }
    }

    :param color: a RGB color tuple eg. [(255, 255, 255), (0, 0, 0)]
    :returns: Adobe ASE swatch dictionary
    """
    r, g, b = color
    return {
        "name": rgb_2_hex(color),
        "type": "Process",
        "data": {"mode": "RGB", "values": [r / 255, g / 255, b / 255]},
    }


def create_ase_swatches(colors: list) -> list:
    """
    Create a list of Adobe ASE swatchs.

    :param colors: a list of RGB color tuples eg. [(255, 255, 255), (0, 0, 0)]
    :returns: formatted Adobe ASE color swatches
    """
    return [format_ase_swatch(color) for color in colors]


def color_byte_chunk(color: dict) -> bytes:
    """
    Build up a byte-chunk for a color in the correct
    format required for an Adobe ASE file.

    credit: https://github.com/nsfmc/swatch

    :returns: byte-chunk for a color
    """
    title = color["name"] + "\0"
    title_length = len(title)
    # Big-Endian Unsigned Short == len(color_name)
    chunk = struct.pack(">H", title_length)
    # UTF-16BE Encoded color_name terminated with '\0'
    chunk += title.encode("utf-16be")
    # grab the color information
    mode = color["data"]["mode"].encode()
    values = color["data"]["values"]
    # encode the color mode
    padded_mode = mode.decode().ljust(4).encode()
    # the color mode
    chunk += struct.pack("!4s", padded_mode)
    # the color values
    chunk += struct.pack("!fff", *values)
    # encode the color type `Process`
    chunk += struct.pack(">h", 2)
    # prepend the chunk size
    chunk = struct.pack(">I", len(chunk)) + chunk
    # retrun the swatch color header + swatch bytes
    return b"\x00\x01" + chunk


def colors_to_bytes(colors: list) -> bytes:
    """
    Converts a list of swatches to bytes suitable for writing.

    credit: https://github.com/nsfmc/swatch

    :returns: bytes for writing complete Adobe ASE file
    """
    header = b"ASEF"
    v_major, v_minor = 1, 0
    chunk_count = len(colors)
    head = struct.pack("!4sHHI", header, v_major, v_minor, chunk_count)
    body = b"".join([color_byte_chunk(color) for color in colors])
    return head + body


def write_ase_file(colors: list) -> object:
    """
    Writes an encoded Adobe ASE file to temporary file object.

    :param colors: a list of RGB color tuples (or lists)
    :returns: temporary file object
    """
    swatches = create_ase_swatches(colors)
    file = tempfile.TemporaryFile()
    file.write(colors_to_bytes(swatches))
    file.seek(0)
    return file


def check_path_type(path):
    """Check to see if a file name was supplied with the path"""
    fn = os.path.basename(path)
    if fn:
        return path + ".SWATCHER"
    else:
        return os.path.join(path, "SWATCHER")


def export_ase_file(colors: list, path: str) -> str:
    """
    Export an encoded Adobe ASE temp file to filesystem.

    :param colors: a list of RGB color tuples (or lists)
    :param `path`: a filename string
    :returns: export location in filesystem
    :exception OSError: swatches could not be exported
    """
    temp_file = write_ase_file(colors)
    fp = check_path_type(path) + ".ase"
    try:
        with open(fp, "wb") as file:
            file.write(temp_file.read())
    except OSError as e:
        raise OSError(f"Swatches could not be exported to {path}.") from e
    return fp


def export_image_file(image: object, path: str) -> str:
    """
    Writes an image of the palette to the filesystem.

    :param image: a PIL image object
    :param `path`: a filename string
    :returns: export location in filesystem
    """
    fp = check_path_type(path) + ".png"
    image.save(fp, "PNG")
    return fp
