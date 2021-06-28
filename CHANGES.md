# swatcher Change Log

**1.0.0** (2021-06-25)

- First official release!

**1.0.1** (2021-06-26)

- Renamed function `resamle()` to `sample()`
- Updated README to reflect the update and fix type

**1.0.2** (2021-06-28)

- Removed `self._location` and `self._filename` and replaced it with `self.path` to simplify
- Removed filename variable from both export functions
    - If a file path string was provided at initialization the file will be exported as `{original_image_name}.SWATCHER.xxx`
    - If a file object was provided at initialization the file will be saved as `{timestamp}.SWATCHER.xxx`
- Updated bug fix for `sensitivity` of 0
- Updated `draw_swatches()`...
    - New function to determine best column and row layout
    - Changed file type from JPEG to PNG with transparency
- Updated tests to reflect changes
- Updated README to reflect changes