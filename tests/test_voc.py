from pathlib import Path

from kili_formats.format.voc import convert_from_kili_to_voc_format

xml_str = '<?xml version="1.0" ?>\n<annotation>\n   <folder/>\n   <filename>filename.xml</filename>\n   <path/>\n   <source>\n      <database>Kili Technology</database>\n   </source>\n   <size>\n      <width>1920</width>\n      <height>1080</height>\n      <depth>3</depth>\n   </size>\n   <segmented/>\n   <object>\n      <name>OBJECT_A</name>\n      <job_name>JOB_0</job_name>\n      <pose>Unspecified</pose>\n      <truncated>0</truncated>\n      <difficult>0</difficult>\n      <occluded>0</occluded>\n      <bndbox>\n         <xmin>317</xmin>\n         <xmax>1609</xmax>\n         <ymin>281</ymin>\n         <ymax>863</ymax>\n      </bndbox>\n   </object>\n</annotation>\n'


def test_voc_convert_from_kili_to_voc_format():
    """Test the conversion from Kili format to VOC format."""

    response = {
        "JOB_0": {
            "annotations": [
                {
                    "categories": [{"confidence": 100, "name": "OBJECT_A"}],
                    "jobName": "JOB_0",
                    "mid": "2022040515434712-7532",
                    "mlTask": "OBJECT_DETECTION",
                    "boundingPoly": [
                        {
                            "normalizedVertices": [
                                {"x": 0.16504140348233334, "y": 0.7986938935103378},
                                {"x": 0.16504140348233334, "y": 0.2605618833516984},
                                {"x": 0.8377886490672706, "y": 0.2605618833516984},
                                {"x": 0.8377886490672706, "y": 0.7986938935103378},
                            ]
                        }
                    ],
                    "type": "rectangle",
                    "children": {},
                }
            ]
        }
    }

    width = 1920
    height = 1080
    parameters = {
        "filename": "filename.xml",
    }

    xmlstr = convert_from_kili_to_voc_format(response, width, height, parameters, None)
    expected_annotation = Path("./tests/expected/object_A_with_0_rotation.xml").read_text(
        encoding="utf-8"
    )
    assert xmlstr == expected_annotation


def test_voc_skips_the_annotations_with_no_bounding_polygon():
    """A point or a line has no box: it is left out, and the job's boxes are still written."""
    box = {
        "categories": [{"confidence": 100, "name": "OBJECT_A"}],
        "boundingPoly": [
            {
                "normalizedVertices": [
                    {"x": 0.16504140348233334, "y": 0.7986938935103378},
                    {"x": 0.16504140348233334, "y": 0.2605618833516984},
                    {"x": 0.8377886490672706, "y": 0.2605618833516984},
                    {"x": 0.8377886490672706, "y": 0.7986938935103378},
                ]
            }
        ],
        "type": "rectangle",
    }
    response = {
        "JOB_0": {"annotations": [box]},
        "POINT_JOB": {
            "annotations": [
                {"categories": [{"name": "TIP"}], "point": {"x": 0.5, "y": 0.5}, "type": "marker"}
            ]
        },
        "LINE_JOB": {
            "annotations": [
                {
                    "categories": [{"name": "EDGE"}],
                    "polyline": [{"x": 0.1, "y": 0.1}, {"x": 0.2, "y": 0.2}],
                    "type": "polyline",
                }
            ]
        },
    }

    xmlstr = convert_from_kili_to_voc_format(
        response, 1920, 1080, {"filename": "filename.xml"}, None
    )

    assert xmlstr == Path("./tests/expected/object_A_with_0_rotation.xml").read_text(
        encoding="utf-8"
    )
