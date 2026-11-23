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
    pdf_asset_with_entities,
    pdf_asset_with_fragments,
    pdf_project,
    pdf_project_asset_unnormalized,
    rectangle,
)
from .fakes.text import text_asset, text_project, text_project_asset_unnormalized
from .fakes.video import video_asset, video_project, video_project_asset_unnormalized


def test_kili_convert_to_pixel_coords_pdf():
    """Test the conversion of coordinates from normalized to pixel values for PDF files."""
    scaled_asset = convert_to_pixel_coords(pdf_asset, pdf_project, normalized_coordinates=False)
    assert scaled_asset == pdf_project_asset_unnormalized


def _pdf_fragments(asset):
    return [
        entity["annotations"][0]
        for entity in asset["latestLabel"]["jsonResponse"]["OBJECT_DETECTION_JOB"]["annotations"]
    ]


_PAGE_RESOLUTIONS = [
    {"pageNumber": 1, "width": 600, "height": 800, "rotation": 0},
    {"pageNumber": 2, "width": 1000, "height": 2000, "rotation": 0},
]


def test_kili_convert_to_pixel_coords_pdf_scales_each_ring_with_its_own_page():
    """A multi-page entity: each ring with its page's size, boundingPoly with its own pages."""
    asset = pdf_asset_with_entities(
        [
            (
                [
                    rectangle(0.25, 0.75, 0.5, 0.875),
                    rectangle(0.5, 0.75, 0.75, 0.875),
                    rectangle(0.25, 0.125, 0.5, 0.25),
                ],
                [1, 1, 2],
                [rectangle(0.25, 0.75, 0.75, 0.875), rectangle(0.25, 0.125, 0.5, 0.25)],
                [1, 2],
            )
        ],
        _PAGE_RESOLUTIONS,
    )

    convert_to_pixel_coords(asset, pdf_project)

    [fragment] = _pdf_fragments(asset)
    assert fragment["polys"][0]["vertices"] == [
        rectangle(150, 600, 300, 700),
        rectangle(300, 600, 450, 700),
        rectangle(250, 250, 500, 500),
    ]
    assert fragment["boundingPoly"][0]["vertices"] == [
        rectangle(150, 600, 450, 700),
        rectangle(250, 250, 500, 500),
    ]


def test_kili_convert_to_pixel_coords_pdf_without_page_resolutions():
    """A PDF nobody opened has no page sizes: its polygons keep their normalizedVertices only."""
    asset = pdf_asset_with_entities(
        [([rectangle(0.25, 0.75, 0.5, 0.875)], [1], [rectangle(0.25, 0.75, 0.5, 0.875)], [1])],
        None,
    )

    convert_to_pixel_coords(asset, pdf_project)

    [fragment] = _pdf_fragments(asset)
    assert fragment["polys"] == [{"normalizedVertices": [rectangle(0.25, 0.75, 0.5, 0.875)]}]
    assert fragment["boundingPoly"] == [{"normalizedVertices": [rectangle(0.25, 0.75, 0.5, 0.875)]}]


def test_kili_convert_to_pixel_coords_pdf_on_a_page_without_size():
    """Only the polygons on a page without a size keep their normalizedVertices only."""
    asset = pdf_asset_with_entities(
        [
            ([rectangle(0.25, 0.75, 0.5, 0.875)], [1], [rectangle(0.25, 0.75, 0.5, 0.875)], [1]),
            ([rectangle(0.25, 0.125, 0.5, 0.25)], [2], [rectangle(0.25, 0.125, 0.5, 0.25)], [2]),
            (
                [rectangle(0.25, 0.75, 0.5, 0.875), rectangle(0.25, 0.125, 0.5, 0.25)],
                [1, 2],
                [rectangle(0.25, 0.75, 0.5, 0.875), rectangle(0.25, 0.125, 0.5, 0.25)],
                [1, 2],
            ),
        ],
        _PAGE_RESOLUTIONS[:1],
    )

    convert_to_pixel_coords(asset, pdf_project)

    on_page_1, on_page_2, on_both_pages = _pdf_fragments(asset)
    assert on_page_1["polys"][0]["vertices"] == [rectangle(150, 600, 300, 700)]
    assert on_page_1["boundingPoly"][0]["vertices"] == [rectangle(150, 600, 300, 700)]
    for fragment in (on_page_2, on_both_pages):
        assert "vertices" not in fragment["polys"][0]
        assert "vertices" not in fragment["boundingPoly"][0]


def test_kili_convert_to_pixel_coords_pdf_older_fragments():
    """Older fragments: one flat ring per polygon, a scalar pageNumber, or a short page array."""
    on_page_1 = rectangle(0.25, 0.75, 0.5, 0.875)
    on_page_2 = rectangle(0.25, 0.125, 0.5, 0.25)
    asset = pdf_asset_with_fragments(
        [
            {
                "boundingPoly": [
                    {"normalizedVertices": on_page_1},
                    {"normalizedVertices": on_page_2},
                ],
                "pageNumberArray": [1, 2],
                "polys": [{"normalizedVertices": on_page_1}, {"normalizedVertices": on_page_2}],
            },
            {
                "boundingPoly": [{"normalizedVertices": [on_page_2]}],
                "pageNumber": 2,
                "polys": [{"normalizedVertices": [on_page_2]}],
            },
            {
                "boundingPoly": [{"normalizedVertices": [on_page_1]}],
                "polys": [{"normalizedVertices": [on_page_1, on_page_1]}],
                "pageNumberArray": [2],
            },
        ],
        _PAGE_RESOLUTIONS,
    )

    convert_to_pixel_coords(asset, pdf_project)

    one_ring_per_polygon, scalar_page_number, short_page_array = _pdf_fragments(asset)
    assert [polygon["vertices"] for polygon in one_ring_per_polygon["polys"]] == [
        rectangle(150, 600, 300, 700),
        rectangle(250, 250, 500, 500),
    ]
    assert scalar_page_number["polys"][0]["vertices"] == [rectangle(250, 250, 500, 500)]
    assert short_page_array["polys"][0]["vertices"] == [
        rectangle(250, 1500, 500, 1750),
        rectangle(150, 600, 300, 700),
    ]


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
