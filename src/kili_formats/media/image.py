"""Tools for export with images."""

import struct
from pathlib import Path
from typing import Dict, Optional, Tuple

from kili_formats.exceptions import NotExportableAssetError, UnidentifiedImageError

# An ICO directory entry stores each side on a single byte, where 0 means 256.
_ICO_HEADER_SIZE = 6
_ICO_ENTRY_SIZE = 16
_ICO_MAX_SIDE = 256


def _read_ico_dimensions(filepath: str) -> Optional[Tuple[int, int]]:
    """Read an ICO directory, which imagesize does not cover.

    Only the header is read, never the pixels. An ICO holds several images, and
    Pillow reports the largest one, so this does the same. Returns None when the
    file is not a readable ICO, leaving the caller to report it.
    """
    with Path(filepath).open("rb") as file:
        header = file.read(_ICO_HEADER_SIZE)
        if len(header) < _ICO_HEADER_SIZE:
            return None
        reserved, image_type, entry_count = struct.unpack("<HHH", header)
        if reserved != 0 or image_type != 1 or entry_count == 0:
            return None
        entries = file.read(_ICO_ENTRY_SIZE * entry_count)

    if len(entries) < _ICO_ENTRY_SIZE * entry_count:
        return None

    sizes = [
        (
            entries[_ICO_ENTRY_SIZE * index] or _ICO_MAX_SIDE,
            entries[_ICO_ENTRY_SIZE * index + 1] or _ICO_MAX_SIDE,
        )
        for index in range(entry_count)
    ]
    return max(sizes, key=lambda size: size[0] * size[1])


def get_image_dimensions_from_file(filepath: str) -> Tuple:
    """Get an image width and height, reading its header only.

    Raises:
        UnidentifiedImageError: the file is not an image we can measure.
    """
    try:
        import imagesize  # pylint: disable=import-outside-toplevel
    except ImportError as error:
        raise ImportError(
            "Install with `pip install kili-formats[image]` to use this feature."
        ) from error

    try:
        width, height = imagesize.get(filepath)
    except (struct.error, ValueError):
        # A truncated or malformed header; fall through to the ICO reader.
        width, height = -1, -1

    if width > 0 and height > 0:
        return int(width), int(height)

    ico_dimensions = _read_ico_dimensions(filepath)
    if ico_dimensions is not None:
        return ico_dimensions

    raise UnidentifiedImageError(f"Cannot read the dimensions of '{filepath}'.")


def get_image_dimensions(asset: Dict) -> Tuple:
    """Get an asset image width and height."""
    if "resolution" in asset and asset["resolution"] is not None:
        return (asset["resolution"]["width"], asset["resolution"]["height"])

    if Path(asset["content"]).is_file():
        return get_image_dimensions_from_file(asset["content"])

    raise NotExportableAssetError(
        f"Could not find dimensions for asset with externalId '{asset['externalId']}'. Please"
        " use `kili.update_properties_in_assets()` to update the resolution of your asset. Or use"
        " `kili.export_labels(with_assets=True).`"
    )


def get_frame_dimensions(asset: Dict) -> Tuple:
    """Get a video asset frame width and height."""
    if "resolution" in asset and asset["resolution"] is not None:
        return (asset["resolution"]["width"], asset["resolution"]["height"])

    if (
        isinstance(asset["jsonContent"], list)
        and len(asset["jsonContent"]) > 0
        and Path(asset["jsonContent"][0]).is_file()
    ):
        return get_image_dimensions_from_file(asset["jsonContent"][0])

    raise NotExportableAssetError(
        f"Could not find dimensions for asset with externalId '{asset['externalId']}'. Please"
        " use `kili.update_properties_in_assets()` to update the resolution of your asset. Or use"
        " `kili.export_labels(with_assets=True).`"
    )
