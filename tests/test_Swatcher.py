import os
import pytest
import tempfile

from io import BytesIO
from PIL import Image, ImageDraw
from swatcher import Swatcher


def create_test_image_bytes():
    img = Image.new("RGB", (600, 400), (255, 255, 255))
    d = ImageDraw.Draw(img)
    d.rectangle((0, 0, 200, 400), (255, 0, 0))
    d.rectangle((200, 0, 400, 400), (255, 255, 255))
    d.rectangle((400, 0, 600, 400), (0, 0, 255))
    temp = BytesIO()
    img.save(temp, "JPEG", quality=100, subsampling=0)
    return Swatcher(temp)


IMG = create_test_image_bytes()
TEMP_DIR = tempfile.TemporaryDirectory()


def test_01():  # sampled palette with defaults
    assert IMG.palette == [(255, 0, 0), (0, 0, 255), (255, 255, 255)]


def test_02():  # palette_image size with defaults
    assert IMG.palette_image.size == (600, 200)


def test_03():  # processed image size
    assert IMG.processed_image.size == (500, 333)


def test_04():  # setting max_color directly
    IMG.max_colors = 3
    assert IMG.max_colors == 3


def test_05():  # setting max_color directly with bad input
    with pytest.raises(ValueError):
        IMG.max_colors = -100


def test_06():  # setting sensitivity directly
    IMG.sensitivity = 50
    assert IMG.sensitivity == 50


def test_07():  # setting sensitivity directly with bad input
    with pytest.raises(ValueError):
        IMG.sensitivity = 5000


def test_08():  # sampled palette with max_colors=1
    IMG.max_colors = 1
    assert IMG.palette == [(255, 0, 0)]


def test_09():  # sampled palette with max_colors=2
    IMG.sample(max_colors=2)
    assert IMG.palette == [(255, 0, 0), (0, 0, 255)]


def test_10():  # sampled palette with indirect settings in sample function
    IMG.sample(6, 250)
    assert IMG.palette == [(255, 0, 0), (0, 0, 255), (255, 255, 255)]


def test_11():  # image export
    filename = "test_export_image"
    path = IMG.export_palette_image(TEMP_DIR.name, filename)
    assert os.path.exists(path)


def test_12():  # ase export
    filename = "test_export_ase"
    path = IMG.export_ase_file(TEMP_DIR.name, filename)
    assert os.path.exists(path)


def test_13():  # export location does not exist
    with pytest.raises(FileNotFoundError):
        temp_dir_gone = tempfile.TemporaryDirectory()
        temp_dir_gone.cleanup()
        filename = "test_export_fail"
        path = IMG.export_ase_file(temp_dir_gone.name, filename)
