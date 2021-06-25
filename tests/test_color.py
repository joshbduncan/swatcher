from swatcher import color


def test_01():  # normalize_rgb_values function
    assert color.normalize_rgb_values((1, 1, 1)) == (0, 0, 0)


def test_02():  # normalize_rgb_values function
    assert color.normalize_rgb_values((253, 253, 253)) == (255, 255, 255)


def test_03():  # normalize_rgb_values function
    assert color.normalize_rgb_values((251, 251, 253)) == (251, 251, 255)


def test_04():  # rgb_2_luma function
    assert color.rgb_2_luma((255, 255, 255)) == 0.99


def test_05():  # rgb_2_luma function
    assert color.rgb_2_luma((128, 128, 128)) == 0.5


def test_06():  # sort_by_brightness function
    colors = [(0, 0, 0), (255, 255, 255), (128, 128, 128)]
    assert color.sort_by_brightness(colors) == [
        (255, 255, 255),
        (128, 128, 128),
        (0, 0, 0),
    ]


def test_07():  # rgb_2_hex function
    assert color.rgb_2_hex((250, 112, 20)) == "#fa7014"


def test_08():  # rgb_2_cmyk function
    assert color.rgb_2_cmyk((255, 0, 0)) == (0, 100, 100, 0)


def test_09():  # color_2_dict function
    assert color.color_2_dict((128, 128, 128)) == {
        "rgb": (128, 128, 128),
        "hex": "#808080",
        "cmyk": (0, 0, 0, 49),
    }


def test_10():  # color distance calcuation
    assert color.color_distance((0, 0, 0), (255, 255, 255)) == 441


def test_11():  # color distance calcuation
    assert color.color_distance((0, 0, 0), (128, 128, 128)) == 221


def test_12():  # color distance calcuation
    assert color.color_distance((0, 0, 0), (0, 0, 0)) == 0
