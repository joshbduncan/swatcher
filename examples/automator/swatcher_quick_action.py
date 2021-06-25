import sys
from swatcher import Swatcher

files = sys.argv[1:]

for file in files:
    s = Swatcher(file)
    s.sample(max_colors=10)
    s.export_palette_image()
    s.export_ase_file()
