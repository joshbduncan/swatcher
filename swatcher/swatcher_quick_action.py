import sys
from swatcher import Swatcher


if __name__ == "__main__":
    files = sys.argv[1:]

    for file in files:
        s = Swatcher(file)
        s.export_ase_file()
        s.export_palette_image()
