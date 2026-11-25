import json
from datetime import datetime

import pytest

from kili_formats.layout import (
    ONTOLOGY_MANIFEST_FILE,
    LabelFile,
    OntologyVersions,
    YoloFolder,
    asset_label_files,
    exported_jobs,
    frame_name,
    image_filename,
    keep_labels_of_version,
    label_frame_count,
    label_suffix,
    labels_of,
    one_asset_per_label,
    ontology_file,
    ontology_manifest,
    ontology_snapshot,
    readme,
    video_metadata,
    with_annotation_types,
    write_ontology_versions,
    yolo_class_file,
    yolo_folders,
    yolo_label_file,
    yolo_label_filename,
    yolo_readme_notes,
    yolo_tasks,
)
from kili_formats.types import JobCategory


def _job(*tools, categories=("A", "B"), **extra):
    return {
        "mlTask": "OBJECT_DETECTION",
        "tools": list(tools),
        "content": {"categories": {name: {"name": name} for name in categories}},
        **extra,
    }


INTERFACE = {
    "jobs": {
        "BOX_JOB": _job("rectangle"),
        "POLYGON_JOB": _job("polygon", categories=("C",)),
        "MASK_JOB": _job("semantic", categories=("D",)),
        "POINT_JOB": _job("marker"),
        "MODEL_JOB": _job("rectangle", isModel=True),
        "CLASSIFICATION_JOB": {"mlTask": "CLASSIFICATION", "content": {"categories": {}}},
    }
}

BOX = {
    "type": "rectangle",
    "categories": [{"name": "A"}],
    "boundingPoly": [
        {
            "normalizedVertices": [
                {"x": 0.1, "y": 0.3},
                {"x": 0.1, "y": 0.1},
                {"x": 0.3, "y": 0.1},
                {"x": 0.3, "y": 0.3},
            ]
        }
    ],
}
TRIANGLE = {
    "type": "polygon",
    "categories": [{"name": "C"}],
    "boundingPoly": [
        {"normalizedVertices": [{"x": 0.5, "y": 0.1}, {"x": 0.7, "y": 0.4}, {"x": 0.3, "y": 0.4}]}
    ],
}
RESPONSE = {"BOX_JOB": {"annotations": [BOX]}, "POLYGON_JOB": {"annotations": [TRIANGLE]}}


@pytest.mark.parametrize(
    ("label_format", "jobs"),
    [
        ("coco", ["BOX_JOB", "POLYGON_JOB", "MASK_JOB"]),
        ("pascal_voc", ["BOX_JOB"]),
        ("yolo", ["BOX_JOB", "POLYGON_JOB", "MASK_JOB"]),
        ("yolo_v4", ["BOX_JOB"]),
        ("yolo_v8", ["BOX_JOB", "POLYGON_JOB", "MASK_JOB"]),
    ],
)
def test_each_format_exports_its_shapes_jobs_models_aside(label_format, jobs):
    assert list(exported_jobs(INTERFACE, label_format)) == jobs


def test_an_asset_has_its_latest_labels_per_step_and_all_its_labels():
    asset = {"latestLabel": {"id": 1}, "latestLabels": [{"id": 2}, None], "labels": [{"id": 3}]}

    assert [label["id"] for label in labels_of(asset)] == [1, 2, 3]
    assert labels_of({"latestLabel": None}) == []


def test_several_labels_are_suffixed_a_single_one_is_not():
    assert [label_suffix(index, 2) for index in (1, 2)] == ["_label1", "_label2"]
    assert label_suffix(1, 1) == ""


def test_an_asset_is_copied_once_per_label_its_image_shared():
    asset = {"externalId": "car", "content": "car.jpg", "latestLabels": [{"id": 1}, {"id": 2}]}

    copies = one_asset_per_label(asset)

    assert [
        (copy["externalId"], copy["content"], copy["latestLabel"]["id"]) for copy in copies
    ] == [
        ("car", "car.jpg", 1),
        ("car", "car.jpg", 2),
    ]
    assert all("latestLabels" not in copy for copy in copies)


@pytest.mark.parametrize(
    ("name", "content_type", "filename"),
    [
        ("car", "image/png; charset=binary", "car.png"),
        ("car", "image/jpg", "car.jpg"),
        ("car.jpg", "image/png", "car.jpg"),
        ("scan.TIF", "image/tiff", "scan.TIF"),
        ("car.v2", None, "car.v2"),
        ("car.json", "image/png", "car.json.png"),
        ("car", "application/octet-stream", "car"),
        ("doc.pdf", "application/pdf", "doc.pdf"),
        ("clip", "video/mp4", "clip.mp4"),
        ("logo.svg", "image/svg+xml", "logo.svg"),
        ("dir/car", "image/png", "dir/car.png"),
        ("../../tmp/car", "image/png", "tmp/car.png"),
        ("/etc/car", "image/png", "etc/car.png"),
    ],
)
def test_a_downloaded_media_takes_the_extension_of_its_content_type(name, content_type, filename):
    assert image_filename(name, content_type) == filename


def test_a_frame_is_numbered_from_1_to_the_width_of_the_frame_count():
    assert frame_name("video", 6, 120) == "video_007"
    assert frame_name("video", 0, 9) == "video_1"


@pytest.mark.parametrize(
    ("external_id", "name"),
    [
        ("dir/car", "dir/car"),
        ("../../car", "car"),
        ("/a/./b//car", "a/b/car"),
        ("a\\car", "a/car"),
        ("..", "_"),
    ],
)
def test_an_external_id_names_files_inside_the_export(external_id, name):
    asset = {"externalId": external_id, "latestLabel": {"jsonResponse": RESPONSE}}

    assert asset_label_files(asset, "IMAGE", ["BOX_JOB"]) == [LabelFile(name, name, None, RESPONSE)]


def test_an_image_gets_a_file_per_label_its_image_shared():
    asset = {
        "externalId": "car",
        "latestLabels": [{"jsonResponse": RESPONSE}, {"jsonResponse": {}}],
    }

    assert asset_label_files(asset, "IMAGE", ["BOX_JOB"]) == [
        LabelFile("car_label1", "car", None, RESPONSE),
        LabelFile("car_label2", "car", None, {}),
    ]


@pytest.mark.parametrize("key", [str, int])
def test_a_video_gets_a_file_per_frame_with_a_shape_of_the_jobs(key):
    label = {
        "jsonResponse": {
            key(0): {},
            key(1): RESPONSE,
            key(2): {"POLYGON_JOB": {"annotations": [TRIANGLE]}},
            "assetLevel": {"CLASSIFICATION_JOB": {}},
        }
    }

    files = asset_label_files(
        {"externalId": "vid", "latestLabel": label}, "VIDEO", ["BOX_JOB"], 120
    )

    assert files == [LabelFile("vid_002", "vid_002", 1, RESPONSE)]


def test_a_video_frame_is_named_after_the_frames_its_labels_cover_when_not_known():
    label = {"jsonResponse": {str(f): RESPONSE for f in range(10)}, "assetLevel": {}}

    files = asset_label_files({"externalId": "vid", "latestLabel": label}, "VIDEO", ["BOX_JOB"])

    assert label_frame_count(label) == 10
    assert [file.stem for file in files][:2] == ["vid_01", "vid_02"]


def test_a_video_label_with_no_frame_gets_no_file():
    asset = {"externalId": "vid", "latestLabel": {"jsonResponse": {}}}

    assert asset_label_files(asset, "VIDEO", ["BOX_JOB"], 5) == []


def test_an_annotation_without_a_type_takes_its_job_single_shape_tool():
    untyped = {key: value for key, value in BOX.items() if key != "type"}

    typed = with_annotation_types({"BOX_JOB": {"annotations": [untyped]}}, INTERFACE)

    assert typed["BOX_JOB"]["annotations"][0]["type"] == "rectangle"


@pytest.mark.parametrize(
    ("label_format", "bounding_boxes", "tasks"),
    [
        ("yolo", "box", ["detect", "segment"]),
        ("yolo", "obb", ["obb", "segment"]),
        ("yolo", "polygon", ["segment"]),
        ("yolo_v8", "obb", ["obb", "segment"]),
        ("yolo_v4", "obb", ["detect"]),
    ],
)
def test_a_yolo_export_writes_the_boxes_task_then_segment(label_format, bounding_boxes, tasks):
    assert yolo_tasks(INTERFACE, label_format, bounding_boxes) == tasks


@pytest.mark.parametrize("split", [False, True])
@pytest.mark.parametrize("bounding_boxes", ["box", "obb", "polygon"])
def test_yolo_lays_out_the_files_of_the_deprecated_yolo_v8(split, bounding_boxes):
    folders = yolo_folders(INTERFACE, "yolo", split=split, bounding_boxes=bounding_boxes)

    assert folders == yolo_folders(INTERFACE, "yolo_v8", split=split, bounding_boxes=bounding_boxes)
    assert [yolo_class_file(folder, "yolo") for folder in folders.values()] == [
        yolo_class_file(folder, "yolo_v8") for folder in folders.values()
    ]


def test_a_merged_yolo_export_writes_a_folder_per_task():
    folders = yolo_folders(INTERFACE, "yolo_v8", split=False, bounding_boxes="obb")

    assert {path: (folder.task, folder.boxes_as_polygons) for path, folder in folders.items()} == {
        "obb": ("obb", False),
        "segment": ("segment", False),
    }
    assert [(c.job_id, c.category_name, c.id) for c in folders["segment"].categories.values()] == [
        ("POLYGON_JOB", "C", 0),
        ("MASK_JOB", "D", 1),
    ]


def test_a_merged_yolo_export_with_one_task_writes_it_at_the_root():
    folders = yolo_folders(INTERFACE, "yolo_v8", split=False, bounding_boxes="polygon")

    (folder,) = folders.values()
    assert list(folders) == [""]
    assert folder.boxes_as_polygons
    assert [category.id for category in folder.categories.values()] == [0, 1, 2, 3]


def test_a_split_yolo_export_writes_each_job_for_its_own_task():
    folders = yolo_folders(
        {"jobs": {**INTERFACE["jobs"], "BOTH_JOB": _job("rectangle", "polygon")}},
        "yolo_v8",
        split=True,
        bounding_boxes="obb",
    )

    assert {path: (folder.task, folder.boxes_as_polygons) for path, folder in folders.items()} == {
        "BOX_JOB": ("obb", False),
        "POLYGON_JOB": ("segment", True),
        "MASK_JOB": ("segment", True),
        "BOTH_JOB": ("segment", True),
    }
    assert not any(folder.with_job for folder in folders.values())


def test_a_split_yolo_export_with_boxes_as_polygons_writes_the_box_job_for_segment():
    folders = yolo_folders(INTERFACE, "yolo_v8", split=True, bounding_boxes="polygon")

    assert (folders["BOX_JOB"].task, folders["BOX_JOB"].boxes_as_polygons) == ("segment", True)


CATEGORIES = {
    "BOX_JOB__A": JobCategory(category_name="A", id=0, job_id="BOX_JOB"),
    "POLYGON_JOB__C": JobCategory(category_name="C", id=1, job_id="POLYGON_JOB"),
}


@pytest.mark.parametrize(
    ("label_format", "with_job", "class_file"),
    [
        (
            "yolo",
            True,
            (
                "data.yaml",
                'train: images\nval: images\nnc: 2\nnames: ["BOX_JOB/A", "POLYGON_JOB/C"]\n',
            ),
        ),
        ("yolo", False, ("data.yaml", 'train: images\nval: images\nnc: 2\nnames: ["A", "C"]\n')),
        ("yolo_v4", True, ("classes.txt", "0 BOX_JOB/A\n1 POLYGON_JOB/C\n")),
        (
            "yolo_v5",
            True,
            (
                "data.yaml",
                'train: images\nval: images\nnames:\n  0: "BOX_JOB/A"\n  1: "POLYGON_JOB/C"\n',
            ),
        ),
        (
            "yolo_v8",
            True,
            (
                "data.yaml",
                'train: images\nval: images\nnc: 2\nnames: ["BOX_JOB/A", "POLYGON_JOB/C"]\n',
            ),
        ),
        ("yolo_v8", False, ("data.yaml", 'train: images\nval: images\nnc: 2\nnames: ["A", "C"]\n')),
    ],
)
def test_the_class_file_of_each_yolo_version(label_format, with_job, class_file):
    folder = YoloFolder("segment", CATEGORIES, with_job=with_job)

    assert yolo_class_file(folder, label_format) == class_file


def test_a_class_name_yaml_would_read_otherwise_stays_a_name():
    folder = YoloFolder("detect", {"J__NO": JobCategory(category_name="NO", id=0, job_id="J")})

    assert yolo_class_file(folder, "yolo_v5")[1].endswith('  0: "J/NO"\n')


def test_a_dataset_in_a_folder_finds_the_shared_images_above_it():
    folders = yolo_folders(INTERFACE, "yolo_v8", split=False)

    assert {path: folder.images for path, folder in folders.items()} == {
        "detect": "../images",
        "segment": "../images",
    }
    assert yolo_readme_notes(folders)
    assert not yolo_readme_notes(yolo_folders(INTERFACE, "yolo_v4", split=False))


def test_a_label_file_is_named_after_its_image_its_extension_aside():
    assert yolo_label_filename("car.JPG") == "car.txt"
    assert yolo_label_filename("scan.tif") == "scan.txt"
    assert yolo_label_filename("car.v2") == "car.v2.txt"
    assert yolo_label_filename("video_007") == "video_007.txt"


def test_a_label_file_holds_a_line_per_shape_of_the_folder_jobs_for_its_task():
    segment = YoloFolder("segment", CATEGORIES, boxes_as_polygons=True)

    assert yolo_label_file(RESPONSE, segment) == (
        "0 0.1 0.3 0.1 0.1 0.3 0.1 0.3 0.3\n1 0.5 0.1 0.7 0.4 0.3 0.4\n"
    )
    assert yolo_label_file({}, segment) == ""


def test_the_video_metadata_lists_each_video_frames():
    assert video_metadata({"b": ["b_1"], "a": ["a_1"]}) == (
        '{\n    "a": [\n        "a_1"\n    ],\n    "b": [\n        "b_1"\n    ]\n}'
    )


def test_the_readme_describes_the_export():
    project = {"title": "Cars", "id": "p1", "description": "Some cars"}

    assert readme(project, "yolo_v8", "latest", datetime(2026, 10, 15, 9, 30)) == (
        "Exported Labels from KILI\n=========================\n\n- Project name: Cars\n"
        "- Project identifier: p1\n- Project description: Some cars\n"
        "- Export date: 20261015-093000\n- Exported format: yolo_v8\n- Exported labels: latest\n"
    )


def test_the_readme_of_a_project_with_no_description_leaves_it_empty():
    project = {"title": "Cars", "id": "p1", "description": None}

    assert "- Project description: \n" in readme(project, "yolo_v8", "latest")


def _label(version, **extra):
    return {"jsonResponse": {}, "recordedOntologyVersion": version, **extra}


def test_the_ontology_files_and_their_manifest_share_a_folder():
    assert ontology_file(3) == "ontologies/ontology_v3.json"
    assert ONTOLOGY_MANIFEST_FILE == "ontologies/manifest.json"


def test_keeping_the_labels_of_a_version_leaves_out_the_others_whichever_way_they_were_fetched():
    asset = {
        "latestLabel": _label(1),
        "latestLabels": [_label(2, id="kept"), _label(1), None],
        "labels": [_label(None), _label(2, id="kept too")],
    }

    assert keep_labels_of_version(asset, 2) is True

    assert asset["latestLabel"] is None
    assert [label["id"] for label in asset["latestLabels"]] == ["kept"]
    assert [label["id"] for label in asset["labels"]] == ["kept too"]


def test_keeping_the_labels_of_a_version_says_when_an_asset_has_none_left():
    made_before_versioning = {"latestLabel": _label(None)}
    on_another_version = {"labels": [_label(1)]}
    with_no_label = {"latestLabel": None, "latestLabels": None}

    assert keep_labels_of_version(made_before_versioning, 1) is False
    assert keep_labels_of_version(on_another_version, 2) is False
    assert keep_labels_of_version(with_no_label, 1) is False
    assert made_before_versioning["latestLabel"] is None
    assert on_another_version["labels"] == []
    assert with_no_label["latestLabels"] is None


def test_keeping_the_labels_of_a_version_keeps_a_latest_label_made_with_it():
    asset = {"latestLabel": _label(2)}

    assert keep_labels_of_version(asset, 2) is True
    assert asset["latestLabel"] == _label(2)


def test_a_label_is_exported_with_its_ontology_version_and_with_none_before_versioning():
    asset = {
        "latestLabel": _label(2),
        "latestLabels": [_label(None), None],
        "labels": [{"jsonResponse": {}}],
    }

    write_ontology_versions(asset)

    assert asset["latestLabel"] == {"jsonResponse": {}, "ontologyVersion": 2}
    assert asset["latestLabels"] == [{"jsonResponse": {}, "ontologyVersion": None}, None]
    assert asset["labels"] == [{"jsonResponse": {}, "ontologyVersion": None}]


def test_writing_the_ontology_versions_twice_keeps_them():
    asset = {"latestLabel": _label(2), "labels": None}

    write_ontology_versions(asset)
    write_ontology_versions(asset)

    assert asset["latestLabel"]["ontologyVersion"] == 2


def test_the_ontology_versions_count_the_labels_of_each_and_those_made_before_versioning():
    versions = OntologyVersions()

    versions.add({"latestLabel": _label(3), "labels": [_label(1), _label(3), _label(None)]})
    versions.add({"latestLabels": [_label(1), None]})
    versions.add({"latestLabel": None})

    assert versions.labels == {3: 2, 1: 2}
    assert versions.numbers == [1, 3]
    assert versions.pre_versioning_labels == 1


def test_the_manifest_lists_the_versions_the_current_one_and_the_labels_without_a_version():
    versions = OntologyVersions()
    versions.add({"labels": [_label(3), _label(1), _label(1), _label(None)]})

    assert json.loads(ontology_manifest(versions, 4)) == {
        "currentVersion": 4,
        "ontologyVersionFilter": "all",
        "versions": [
            {"version": 1, "labels": 2, "ontology": "ontologies/ontology_v1.json"},
            {"version": 3, "labels": 1, "ontology": "ontologies/ontology_v3.json"},
        ],
        "preVersioningLabels": 1,
    }


def test_the_manifest_of_an_export_of_the_current_version_says_so():
    versions = OntologyVersions()
    versions.add({"latestLabel": _label(4)})

    manifest = json.loads(ontology_manifest(versions, 4, "current"))

    assert manifest["ontologyVersionFilter"] == "current"
    assert [version["version"] for version in manifest["versions"]] == [4]


def test_the_manifest_of_an_export_with_no_label_lists_no_version():
    manifest = json.loads(ontology_manifest(OntologyVersions(), 2, "current"))

    assert manifest["versions"] == []
    assert manifest["preVersioningLabels"] == 0


@pytest.mark.parametrize(
    "interface",
    [
        '{"jobs": {"JOB": {"mlTask": "CLASSIFICATION"}}}',
        {"jobs": {"JOB": {"mlTask": "CLASSIFICATION"}}},
    ],
)
def test_an_ontology_file_holds_the_interface_whether_fetched_as_a_string_or_parsed(interface):
    assert json.loads(ontology_snapshot(interface)) == {
        "jobs": {"JOB": {"mlTask": "CLASSIFICATION"}}
    }
