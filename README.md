# Swatcher

Swatcher is a Python module for generating Adobe ASE color swatches from images.

## Background

Swatcher was born out of necessity in my day job as a Graphic Designer. 👨‍💻

Often, I need to extract **exact** color values from images for use in Adobe products and I just couldn't find a good way...

> "Isn't there already software that samples colors from images?"

Yeah, there's a bunch, problem is, most are designed for sampling photographs and use algorithms that provide approximate color values. I typically sample computer generated graphics with fairly distinct colors, and, I need **exact** values. 🎯

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

# view image of the sampled palette
s.show_palette_image()

# resample the image with new settings
s.sample(max_colors=4, sensitivity=50)

# export sampled colors as an adobe ase swatch file
s.export_ase_file()

# save an image of the sampled palette swatches
s.export_palette_image()
```

## Resources

- [PyPi](https://pypi.python.org/pypi/swatcher)