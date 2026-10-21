"""Regenerate the binary image fixtures used by ``tests/test_media_image.py``.

Run with any Pillow >= 9:  python tests/assets/generate_fixtures.py

The fixtures are committed as bytes on purpose. Decoding a file that was
encoded by the *running* Pillow would only prove Pillow agrees with itself;
pinning the bytes is what lets the test catch a decoder behaviour change
between Pillow versions.
"""

import struct
from pathlib import Path

from PIL import Image

HERE = Path(__file__).parent

# Distinct, non-square, non-round sizes so a swapped axis or a mixed-up
# fixture shows up as a failure rather than coincidentally matching.
JPEG_SIZE = (97, 61)
PNG_SIZE = (83, 47)
TIFF_SIZE = (71, 53)

# The duplicate-tag TIFF carries ImageWidth/ImageLength twice.
DUP_FIRST = (41, 29)
DUP_SECOND = (97, 61)


def _gradient(size):
    """A non-uniform image: a flat colour would survive almost any decoder bug."""
    width, height = size
    image = Image.new("RGB", size)
    image.putdata(
        [
            ((x * 7) % 256, (y * 11) % 256, (x + y) % 256)
            for y in range(height)
            for x in range(width)
        ]
    )
    return image


def _write_duplicate_tag_tiff(path):
    """Hand-build a little-endian TIFF whose IFD repeats ImageWidth/ImageLength.

    Pillow parses IFD entries sequentially into a dict, so which of the two
    values survives is a pure library-behaviour question: Pillow <= 12 kept the
    last, Pillow >= 13 keeps the first.
    """
    short = 3
    entries = [
        (256, short, DUP_FIRST[0]),  # ImageWidth  (first)
        (256, short, DUP_SECOND[0]),  # ImageWidth  (duplicate)
        (257, short, DUP_FIRST[1]),  # ImageLength (first)
        (257, short, DUP_SECOND[1]),  # ImageLength (duplicate)
        (258, short, 8),  # BitsPerSample
        (259, short, 1),  # Compression: none
        (262, short, 1),  # PhotometricInterpretation: BlackIsZero
        (273, short, 0),  # StripOffsets, patched below
        (277, short, 1),  # SamplesPerPixel
        (278, short, DUP_SECOND[1]),  # RowsPerStrip
        (279, short, 0),  # StripByteCounts, patched below
    ]

    header_len = 8
    ifd_len = 2 + 12 * len(entries) + 4
    strip_offset = header_len + ifd_len
    # Size the strip for the larger of the two candidate sizes so the file is
    # valid whichever one the reader picks.
    strip_len = DUP_SECOND[0] * DUP_SECOND[1]
    entries = [
        (t, ty, strip_offset if t == 273 else strip_len if t == 279 else v) for t, ty, v in entries
    ]

    out = bytearray()
    out += b"II" + struct.pack("<HI", 42, header_len)
    out += struct.pack("<H", len(entries))
    for tag, typ, value in entries:
        # A SHORT lives in the low two bytes of the 4-byte value field.
        out += struct.pack("<HHI", tag, typ, 1) + struct.pack("<HH", value, 0)
    out += struct.pack("<I", 0)  # no next IFD
    out += bytes((i * 3) % 256 for i in range(strip_len))
    path.write_bytes(bytes(out))


def main():
    _gradient(JPEG_SIZE).save(HERE / "smoke.jpg", format="JPEG", quality=85)
    _gradient(PNG_SIZE).save(HERE / "smoke.png", format="PNG")
    _gradient(TIFF_SIZE).save(HERE / "smoke.tiff", format="TIFF")
    _write_duplicate_tag_tiff(HERE / "smoke_duplicate_tags.tiff")
    print("fixtures written to", HERE)


if __name__ == "__main__":
    main()
