from typing import Dict
from kili_formats.types import JobCategory
from kili_formats.format.yolo import convert_from_kili_to_yolo_format
from .fakes.yolo import (
    asset,
    asset_with_0_rotation,
    asset_with_90_rotation,
    asset_with_180_rotation,
    asset_with_270_rotation,
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
