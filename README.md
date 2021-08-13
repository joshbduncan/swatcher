# Swatcher

Swatcher is a Python module for generating Adobe ASE color swatches from images.

## Background

Swatcher was born out of necessity in my day job as a Graphic Designer. 👨‍💻

Often, I need to extract **exact** color values from images for use in Adobe products and I just couldn't find a good way...

> "Isn't there already software that samples colors from images?"

Yeah, there's a bunch, problem is, most are designed for sampling photographs and use algorithms that provide approximate color values. I typically sample computer generated graphics with fairly distinct colors, and I need **exact** values. 🎯

FYI, Swatcher works great on photographs too! 📸

Credit to [Marcos Ojeda](https://github.com/nsfmc/swatch) for his work on the Adobe ASE file writer. 👏

## Installation

Install Swatcher with `pip`:

    pip install swatcher

## Usage

```python
from swatcher import Swatcher

s = Swatcher('/path/to/your/image.jpg')

# view the most common colors (RGB values)
s.palette
```

Swatcher will automatically sample the provided image at initialization using the default settings `max_colors=8` and `sensitivity=75`. I have found these general settings to work best for most images.

ℹ️ You can also specify `max_colors` and `sensitivity` at object creation.

```python
s = Swatcher('/path/to/your/image.jpg', max_colors=5, sensitivity=125)
```

### View the sampled swatches

To view the sample palette swatches in your default system image viewer.

```python
s.show_palette_image()
```

### Resample the image

If the sampled colors were not what you were expecting, you can easily resample your image with different settings.

```python
s.sample(max_colors=4, sensitivity=50)
```

-   **max_colors**: Maximum number of colors to sample (may sample less)
-   **sensitivity**: How perceptively different (Euclidean Distance) a color must be from others to be included in the sampled palette. _A lower value = more similar colors, a higher value = less similar colors._

#### Sensitivity Example:

If you have numerous grey values in your image, reducing the sensitivity will make sure you sample each individual grey. On the flip side, a landscape photograph with a lot of sky will probably sample too many blue values. Increasing the sensitivity will sample a more diverse palette with colors from more areas of the photograph.

### Export an Adobe ASE swatch file

Once you have a palette you like, you can export it to an Adobe ASE swatch file for use in Adobe design products.

```python
s.export_ase_file()
```

By default, the ASE swatch file will be saved in one of two places depending on how you initialized your Swatcher object.

1. If you provided an image file path, the Adobe ASE swatch file will be saved in the same directory.
2. If you provided a file object, the Adobe ASE swatch file will be saved in your current users home directory.

**_...or export to a specific location_**

```python
s.export_ase_file("path/you/want/to/use/")
```

## Resources

-   [PyPi](https://pypi.python.org/pypi/swatcher)
