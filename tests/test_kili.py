import pytest

from kili_formats.exceptions import NotCompatibleOptions
from kili_formats.kili import convert_to_pixel_coords
from .fakes.image import image_asset, image_asset_rotated, image_project, image_project_asset_normalized, image_project_asset_unnormalized, image_rotated_project_asset_unnormalized
from .fakes.pdf import pdf_asset, pdf_asset_rotated, pdf_project, pdf_project_asset_unnormalized
from .fakes.video import video_asset, video_project, video_project_asset_unnormalized

def test_kili_convert_to_pixel_coords_pdf():
    """Test the conversion of coordinates from normalized to pixel values for PDF files."""
    scaled_asset = convert_to_pixel_coords(pdf_asset, pdf_project, normalized_coordinates=False)
    assert scaled_asset == pdf_project_asset_unnormalized

def test_kili_convert_to_pixel_coords_pdf_rotated_throw_error():
    """Test the conversion of coordinates from normalized to pixel values for PDF files raises error if rotated."""
    with pytest.raises(NotCompatibleOptions, match="PDF labels cannot be rotated"):
        convert_to_pixel_coords(pdf_asset_rotated, pdf_project, normalized_coordinates=False)

def test_kili_convert_to_pixel_coords_image():
    """Test the conversion of coordinates from normalized to pixel values for image files."""
    scaled_asset = convert_to_pixel_coords(image_asset, image_project, normalized_coordinates=False)
    assert scaled_asset == image_project_asset_unnormalized

def test_kili_convert_to_pixel_coords_image_with_normalized_coordinates():
    """Test the conversion of coordinates from normalized to pixel values for image files."""
    scaled_asset = convert_to_pixel_coords(image_asset, image_project, normalized_coordinates=True)
    assert scaled_asset == image_project_asset_normalized

def test_kili_convert_to_pixel_coords_video():
    """Test the conversion of coordinates from normalized to pixel values for video files."""
    scaled_asset = convert_to_pixel_coords(video_asset, video_project, normalized_coordinates=False)
    assert scaled_asset == video_project_asset_unnormalized

def test_kili_convert_to_pixel_coords_image_rotated():
    """Test the conversion of coordinates from normalized to pixel values for rotated image files."""
    scaled_asset = convert_to_pixel_coords(
        image_asset_rotated, image_project, normalized_coordinates=False
    )
    assert scaled_asset == image_rotated_project_asset_unnormalized
