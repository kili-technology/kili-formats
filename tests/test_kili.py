import pytest

from kili_formats.exceptions import NotCompatibleOptions
from kili_formats.kili import convert_to_pixel_coords
from src.kili_formats.tool.annotations_to_json_response import (
    AnnotationsToJsonResponseConverter,
)

from .fakes.image import (
    image_asset,
    image_asset_rotated,
    image_project,
    image_project_asset_normalized,
    image_project_asset_unnormalized,
    image_rotated_project_asset_unnormalized,
)
from .fakes.pdf import (
    pdf_asset,
    pdf_asset_rotated,
    pdf_project,
    pdf_project_asset_unnormalized,
)
from .fakes.text import text_asset, text_project, text_project_asset_unnormalized
from .fakes.video import video_asset, video_project, video_project_asset_unnormalized


def test_kili_convert_to_pixel_coords_pdf():
    """Test the conversion of coordinates from normalized to pixel values for PDF files."""
    scaled_asset = convert_to_pixel_coords(pdf_asset, pdf_project, normalized_coordinates=False)
    assert scaled_asset == pdf_project_asset_unnormalized


def test_kili_convert_to_pixel_coords_text():
    """Test the conversion of coordinates from normalized to pixel values for PDF files."""
    scaled_asset = convert_to_pixel_coords(text_asset, text_project, normalized_coordinates=False)
    assert scaled_asset == text_project_asset_unnormalized


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


def test_patch_label_json_response_llm_classic_annotations():
    """Test rebuilding the jsonResponse from annotations for LLM projects.

    LLM projects are the only ones that still rebuild their jsonResponse
    client-side (classification, transcription, comparison, ranking and their
    child jobs). Every other project type is served via jsonResponseUrl.
    """
    json_interface = {
        "jobs": {
            "CLASS_JOB": {"mlTask": "CLASSIFICATION"},
            "CHILD_TRANSCRIPTION": {"mlTask": "TRANSCRIPTION"},
            "TRANSCRIPTION_JOB": {"mlTask": "TRANSCRIPTION"},
        }
    }
    annotations = [
        {
            "__typename": "ClassificationAnnotation",
            "job": "CLASS_JOB",
            "path": [],
            "id": "parent",
            "annotationValue": {"categories": ["A"]},
        },
        {
            "__typename": "TranscriptionAnnotation",
            "job": "CHILD_TRANSCRIPTION",
            "path": [["parent", "A"]],
            "id": "child",
            "annotationValue": {"text": "child text"},
        },
        {
            "__typename": "TranscriptionAnnotation",
            "job": "TRANSCRIPTION_JOB",
            "path": [],
            "id": "flat",
            "annotationValue": {"text": "hello"},
        },
    ]
    label = {"jsonResponse": {}}

    converter = AnnotationsToJsonResponseConverter(
        json_interface=json_interface,
        project_input_type="LLM_STATIC",
    )
    converter.patch_label_json_response(None, label, annotations)

    assert label["jsonResponse"] == {
        "CLASS_JOB": {
            "categories": [
                {"name": "A", "children": {"CHILD_TRANSCRIPTION": {"text": "child text"}}}
            ]
        },
        "TRANSCRIPTION_JOB": {"text": "hello"},
    }


def test_patch_label_json_response_non_llm_is_noop():
    """Non-LLM projects are served via jsonResponseUrl, so no client-side rebuild happens."""
    label = {"jsonResponse": {"EXISTING_JOB": {"text": "kept"}}}
    converter = AnnotationsToJsonResponseConverter(
        json_interface={"jobs": {"SOME_JOB": {}}},
        project_input_type="VIDEO",
    )
    converter.patch_label_json_response(None, label, [])

    assert label["jsonResponse"] == {"EXISTING_JOB": {"text": "kept"}}
