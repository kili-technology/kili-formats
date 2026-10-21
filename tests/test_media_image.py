"""Smoke tests for ``kili_formats.media.image`` against real encoded images.

Every other test in this repository builds its images with ``Image.new(...)``
in memory, which only ever proves that Pillow agrees with itself. These tests
read committed bytes instead, so a change in Pillow's decoders shows up here
rather than on a customer's export.

The fixtures live in ``tests/assets`` and are reproducible with
``python tests/assets/generate_fixtures.py``.
"""

from pathlib import Path

import pytest
from PIL import __version__ as PILLOW_VERSION

from kili_formats.media.image import _get_image_dimensions, get_image_dimensions

ASSETS = Path(__file__).parent / "assets"

PILLOW_MAJOR = int(PILLOW_VERSION.split(".")[0])


@pytest.mark.parametrize(
    ("filename", "expected_dimensions"),
    [
        ("smoke.jpg", (97, 61)),
        ("smoke.png", (83, 47)),
        ("smoke.tiff", (71, 53)),
    ],
)
def test_get_image_dimensions_reads_encoded_files(filename, expected_dimensions):
    """Dimensions come back unchanged for each container we actually ship."""
    assert _get_image_dimensions(str(ASSETS / filename)) == expected_dimensions


def test_get_image_dimensions_on_duplicate_tiff_tags():
    """Pin which duplicated TIFF tag wins, because Pillow 13 swapped it.

    ``smoke_duplicate_tags.tiff`` declares ImageWidth/ImageLength twice, as
    (41, 29) then (97, 61). Pillow <= 12 kept the last occurrence, Pillow >= 13
    keeps the first, so the reported size of a malformed TIFF changes with the
    Pillow major. Well-formed files, covered above, are unaffected.
    """
    expected_dimensions = (41, 29) if PILLOW_MAJOR >= 13 else (97, 61)

    assert _get_image_dimensions(str(ASSETS / "smoke_duplicate_tags.tiff")) == expected_dimensions


def test_get_image_dimensions_falls_back_to_the_file_without_resolution():
    """The public helper decodes the asset content when the API gave no resolution."""
    asset = {"content": str(ASSETS / "smoke.jpg"), "externalId": "smoke"}

    assert get_image_dimensions(asset) == (97, 61)


def test_get_image_dimensions_prefers_the_resolution_over_the_file():
    """A resolution from the API short-circuits decoding, even if it disagrees."""
    asset = {
        "content": str(ASSETS / "smoke.jpg"),
        "externalId": "smoke",
        "resolution": {"width": 1920, "height": 1080},
    }

    assert get_image_dimensions(asset) == (1920, 1080)
