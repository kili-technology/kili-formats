"""Tests for ``kili_formats.media.image`` against real encoded images.

Every other test in this repository builds its images with ``Image.new(...)``
in memory, which only ever proves that the encoder agrees with the decoder.
These tests read committed bytes instead, so a change in how we measure an
image shows up here rather than on a customer's export.

The fixtures live in ``tests/assets`` and are reproducible with
``python tests/assets/generate_fixtures.py``.

Pillow is a test-only dependency here: it is the reference implementation these
tests measure against, and is no longer shipped to users.
"""

from pathlib import Path

import pytest
from PIL import Image

from kili_formats.exceptions import UnidentifiedImageError
from kili_formats.media.image import (
    get_image_dimensions,
    get_image_dimensions_from_file,
)

ASSETS = Path(__file__).parent / "assets"

# Well-formed files, where we must agree with Pillow exactly.
WELL_FORMED = [
    ("smoke.jpg", (97, 61)),
    ("smoke.png", (83, 47)),
    ("smoke.tiff", (71, 53)),
    ("smoke.ico", (48, 48)),
]


@pytest.mark.parametrize(("filename", "expected_dimensions"), WELL_FORMED)
def test_dimensions_of_encoded_files(filename, expected_dimensions):
    """Dimensions come back unchanged for each container we actually ship."""
    assert get_image_dimensions_from_file(str(ASSETS / filename)) == expected_dimensions


@pytest.mark.parametrize(("filename", "_expected_dimensions"), WELL_FORMED)
def test_dimensions_match_pillow(filename, _expected_dimensions):
    """Guard the swap away from Pillow: same answer as the library we dropped."""
    with Image.open(ASSETS / filename) as image:
        assert get_image_dimensions_from_file(str(ASSETS / filename)) == image.size


def test_dimensions_of_duplicate_tiff_tags():
    """Pin which duplicated TIFF tag wins, because the readers disagree.

    ``smoke_duplicate_tags.tiff`` declares ImageWidth/ImageLength twice, as
    (41, 29) then (97, 61). We keep the last occurrence, which is what Pillow
    <= 12 did and therefore what production has always returned. Pillow 13
    switched to the first and would report (41, 29) here, so this file is
    deliberately excluded from the parity test above.
    """
    assert get_image_dimensions_from_file(str(ASSETS / "smoke_duplicate_tags.tiff")) == (97, 61)


def test_unreadable_file_is_reported(tmp_path):
    """A file we cannot measure raises, instead of silently reporting (-1, -1)."""
    not_an_image = tmp_path / "not_an_image.png"
    not_an_image.write_text("certainly not a PNG", encoding="utf-8")

    with pytest.raises(UnidentifiedImageError):
        get_image_dimensions_from_file(str(not_an_image))


def test_truncated_image_is_reported(tmp_path):
    """A header cut in half raises rather than returning half an answer."""
    truncated = tmp_path / "truncated.png"
    truncated.write_bytes((ASSETS / "smoke.png").read_bytes()[:8])

    with pytest.raises(UnidentifiedImageError):
        get_image_dimensions_from_file(str(truncated))


def test_get_image_dimensions_falls_back_to_the_file_without_resolution():
    """The public helper measures the asset content when the API gave no resolution."""
    asset = {"content": str(ASSETS / "smoke.jpg"), "externalId": "smoke"}

    assert get_image_dimensions(asset) == (97, 61)


def test_get_image_dimensions_prefers_the_resolution_over_the_file():
    """A resolution from the API short-circuits reading the file, even if it disagrees."""
    asset = {
        "content": str(ASSETS / "smoke.jpg"),
        "externalId": "smoke",
        "resolution": {"width": 1920, "height": 1080},
    }

    assert get_image_dimensions(asset) == (1920, 1080)
