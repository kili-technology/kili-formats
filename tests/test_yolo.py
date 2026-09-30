from typing import Dict

import pytest

from kili_formats.format.yolo import convert_from_kili_to_yolo_format
from kili_formats.types import JobCategory

from .fakes.yolo import (
    asset,
    asset_with_0_rotation,
    asset_with_90_rotation,
    asset_with_180_rotation,
    asset_with_270_rotation,
    yolo_box,
    yolo_label,
    yolo_mask_part_1,
    yolo_mask_part_2,
    yolo_mask_with_hole,
    yolo_mask_with_two_holes,
    yolo_segment,
    yolo_triangle,
)

job_category_a: JobCategory = JobCategory(category_name="OBJECT_A", id=0, job_id="JOB_0")
job_category_b: JobCategory = JobCategory(category_name="OBJECT_B", id=1, job_id="JOB_0")
category_ids: Dict[str, JobCategory] = {
    "JOB_0__OBJECT_A": job_category_a,
    "JOB_0__OBJECT_B": job_category_b,
}


def test_convert_from_kili_to_yolo_format():
    converted_annotations = convert_from_kili_to_yolo_format(
        "JOB_0", asset["latestLabel"], category_ids
    )
    converted_annotations_with_rotation_0 = convert_from_kili_to_yolo_format(
        "JOB_0", asset_with_0_rotation["latestLabel"], category_ids
    )
    converted_annotations_with_rotation_90 = convert_from_kili_to_yolo_format(
        "JOB_0", asset_with_90_rotation["latestLabel"], category_ids
    )
    converted_annotations_with_rotation_180 = convert_from_kili_to_yolo_format(
        "JOB_0", asset_with_180_rotation["latestLabel"], category_ids
    )
    converted_annotations_with_rotation_270 = convert_from_kili_to_yolo_format(
        "JOB_0", asset_with_270_rotation["latestLabel"], category_ids
    )
    expected_annotations = [
        (
            0,
            0.501415026274802,
            0.5296278884310182,
            0.6727472455849373,
            0.5381320101586394,
        )
    ]
    expected_annotations2 = [
        (0, 0.20836785418392711, 0.28447691496573013, 0.2609776304888154, 0.3803570083603225)
    ]
    assert len(converted_annotations) == 1
    assert converted_annotations == expected_annotations
    assert len(converted_annotations_with_rotation_0) == 1
    assert converted_annotations_with_rotation_0 == expected_annotations2
    assert len(converted_annotations_with_rotation_90) == 1
    assert converted_annotations_with_rotation_90 == expected_annotations2
    assert len(converted_annotations_with_rotation_180) == 1
    assert converted_annotations_with_rotation_180 == expected_annotations2
    assert len(converted_annotations_with_rotation_270) == 1
    assert converted_annotations_with_rotation_270 == expected_annotations2


box_detect_line = (0, 0.2, 0.2, 0.19999999999999998, 0.19999999999999998)
box_segment_line = (0, 0.1, 0.1, 0.3, 0.1, 0.3, 0.3, 0.1, 0.3)
triangle_segment_line = (0, 0.5, 0.1, 0.7, 0.4, 0.3, 0.4)


def _points(line):
    return list(zip(line[1::2], line[2::2]))


def _inside(point, polygon):
    """Even-odd ray casting: what a fill leaves inside."""
    x, y = point
    inside = False
    for (x_1, y_1), (x_2, y_2) in zip(polygon, polygon[1:] + polygon[:1]):
        if (y_1 > y) != (y_2 > y) and x < x_1 + (y - y_1) * (x_2 - x_1) / (y_2 - y_1):
            inside = not inside
    return inside


def test_convert_from_kili_to_yolo_format_without_a_task_mixes_boxes_and_polygons():
    label = yolo_label(yolo_box, yolo_triangle, yolo_mask_with_hole)

    converted = convert_from_kili_to_yolo_format("JOB_0", label, category_ids)

    # As before the option: the mask's outline only.
    assert converted == [
        box_detect_line,
        triangle_segment_line,
        (0, 0.1, 0.5, 0.5, 0.5, 0.5, 0.9, 0.1, 0.9),
    ]


def test_convert_from_kili_to_yolo_format_for_detect_keeps_boxes_only():
    label = yolo_label(yolo_box, yolo_triangle, yolo_mask_with_hole)

    converted = convert_from_kili_to_yolo_format("JOB_0", label, category_ids, task="detect")

    assert converted == [box_detect_line]


def test_convert_from_kili_to_yolo_format_for_segment_writes_polygons_and_box_corners():
    label = yolo_label(yolo_box, yolo_triangle)

    converted = convert_from_kili_to_yolo_format("JOB_0", label, category_ids, task="segment")

    assert converted == [box_segment_line, triangle_segment_line]


def test_convert_from_kili_to_yolo_format_for_segment_keeps_a_hole_empty():
    label = yolo_label(yolo_mask_with_hole)

    [line] = convert_from_kili_to_yolo_format("JOB_0", label, category_ids, task="segment")

    # One ring, the hole joined by a zero-width bridge: filled, the hole stays empty.
    polygon = _points(line)
    assert len(polygon) == 10
    assert _inside((0.15, 0.7), polygon)
    assert not _inside((0.3, 0.7), polygon)


def test_convert_from_kili_to_yolo_format_for_segment_keeps_every_hole_empty():
    label = yolo_label(yolo_mask_with_two_holes)

    [line] = convert_from_kili_to_yolo_format("JOB_0", label, category_ids, task="segment")

    polygon = _points(line)
    assert len(polygon) == 4 + 2 * (4 + 2)
    assert _inside((0.15, 0.85), polygon)
    assert _inside((0.85, 0.15), polygon)
    assert not _inside((0.3, 0.3), polygon)
    assert not _inside((0.6, 0.6), polygon)


def test_convert_from_kili_to_yolo_format_for_segment_writes_a_line_per_mask_part():
    label = yolo_label(yolo_mask_part_1, yolo_mask_part_2)

    converted = convert_from_kili_to_yolo_format("JOB_0", label, category_ids, task="segment")

    assert converted == [(0, 0.6, 0.6, 0.8, 0.6, 0.8, 0.8), (0, 0.6, 0.1, 0.9, 0.1, 0.9, 0.3)]


def test_convert_from_kili_to_yolo_format_for_segment_leaves_out_fewer_than_3_points():
    label = yolo_label(yolo_segment, yolo_triangle)

    converted = convert_from_kili_to_yolo_format("JOB_0", label, category_ids, task="segment")

    assert converted == [triangle_segment_line]


def test_convert_from_kili_to_yolo_format_refuses_an_unknown_task():
    with pytest.raises(ValueError, match="Unknown YOLO task 'SEGMENT'"):
        convert_from_kili_to_yolo_format(
            "JOB_0", yolo_label(yolo_box), category_ids, task="SEGMENT"  # type: ignore
        )
