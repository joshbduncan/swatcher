from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name="swatcher",
    version="1.0.3",
    author="Josh Duncan",
    author_email="joshbduncan@gmail.com",
    description="Generate Adobe ASE swatches from images.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="http://github.com/joshbduncan/swatcher",
    license="MIT",
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    keywords=["adobe", "color", "swatches"],
    packages=find_packages(include=["swatcher"]),
    install_requires=["Pillow"],
    python_requires=">=3.8",
)
