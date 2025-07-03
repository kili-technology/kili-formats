import pytest

from kili_formats.format.geojson import (
    convert_from_kili_to_geojson_format,
    features_to_feature_collection,
    geojson_feature_collection_to_kili_json_response,
    geojson_linestring_feature_to_kili_line_annotation,
    geojson_point_feature_to_kili_point_annotation,
    geojson_polygon_feature_to_kili_bbox_annotation,
    geojson_polygon_feature_to_kili_polygon_annotation,
    geojson_polygon_feature_to_kili_segmentation_annotation,
    kili_bbox_annotation_to_geojson_polygon_feature,
    kili_bbox_to_geojson_polygon,
    kili_json_response_to_feature_collection,
    kili_line_annotation_to_geojson_linestring_feature,
    kili_line_to_geojson_linestring,
    kili_point_annotation_to_geojson_point_feature,
    kili_point_to_geojson_point,
    kili_polygon_annotation_to_geojson_polygon_feature,
    kili_polygon_to_geojson_polygon,
    kili_segmentation_annotation_to_geojson_polygon_feature,
    kili_segmentation_to_geojson_geometry,
)
from kili_formats.format.geojson.exceptions import ConversionError


class TestKiliPointToGeojson:
    def test_kili_point_to_geojson_point(self):
        point = {"x": 1.0, "y": 2.0}
        result = kili_point_to_geojson_point(point)
        expected = {"type": "Point", "coordinates": [1.0, 2.0]}
        assert result == expected

    def test_kili_point_annotation_to_geojson_point_feature(self):
        point_annotation = {
            "children": {},
            "point": {"x": -79.0, "y": -3.0},
            "categories": [{"name": "A"}],
            "mid": "mid_object",
            "type": "marker",
        }
        result = kili_point_annotation_to_geojson_point_feature(point_annotation, "job_name")
        expected = {
            "type": "Feature",
            "geometry": {"type": "Point", "coordinates": [-79.0, -3.0]},
            "id": "mid_object",
            "properties": {
                "kili": {
                    "categories": [{"name": "A"}],
                    "children": {},
                    "type": "marker",
                    "job": "job_name",
                }
            },
        }
        assert result == expected

    def test_kili_point_annotation_to_geojson_point_feature_without_job_name(self):
        point_annotation = {
            "children": {},
            "point": {"x": -79.0, "y": -3.0},
            "categories": [{"name": "A"}],
            "mid": "mid_object",
            "type": "marker",
        }
        result = kili_point_annotation_to_geojson_point_feature(point_annotation)
        expected = {
            "type": "Feature",
            "geometry": {"type": "Point", "coordinates": [-79.0, -3.0]},
            "id": "mid_object",
            "properties": {
                "kili": {"categories": [{"name": "A"}], "children": {}, "type": "marker"}
            },
        }
        assert result == expected

    def test_kili_point_annotation_wrong_type_raises_error(self):
        point_annotation = {
            "children": {},
            "point": {"x": -79.0, "y": -3.0},
            "categories": [{"name": "A"}],
            "mid": "mid_object",
            "type": "rectangle",
        }
        with pytest.raises(AssertionError, match="Annotation type must be `marker`"):
            kili_point_annotation_to_geojson_point_feature(point_annotation)


class TestGeojsonPointToKili:
    def test_geojson_point_feature_to_kili_point_annotation(self):
        point = {
            "type": "Feature",
            "geometry": {"type": "Point", "coordinates": [-79.0, -3.0]},
            "id": "mid_object",
            "properties": {"kili": {"categories": [{"name": "A"}]}},
        }
        result = geojson_point_feature_to_kili_point_annotation(point)
        expected = {
            "children": {},
            "point": {"x": -79.0, "y": -3.0},
            "categories": [{"name": "A"}],
            "mid": "mid_object",
            "type": "marker",
        }
        assert result == expected

    def test_geojson_point_feature_to_kili_point_annotation_with_overrides(self):
        point = {
            "type": "Feature",
            "geometry": {"type": "Point", "coordinates": [-79.0, -3.0]},
            "id": "mid_object",
            "properties": {"kili": {"categories": [{"name": "A"}]}},
        }
        result = geojson_point_feature_to_kili_point_annotation(
            point, categories=[{"name": "B"}], children={"child1": "value"}, mid="new_mid"
        )
        expected = {
            "children": {"child1": "value"},
            "point": {"x": -79.0, "y": -3.0},
            "categories": [{"name": "B"}],
            "mid": "new_mid",
            "type": "marker",
        }
        assert result == expected

    def test_geojson_point_feature_wrong_feature_type_raises_error(self):
        point = {"type": "NotFeature", "geometry": {"type": "Point", "coordinates": [-79.0, -3.0]}}
        with pytest.raises(AssertionError, match="Feature type must be `Feature`"):
            geojson_point_feature_to_kili_point_annotation(point)

    def test_geojson_point_feature_wrong_geometry_type_raises_error(self):
        point = {
            "type": "Feature",
            "geometry": {"type": "LineString", "coordinates": [-79.0, -3.0]},
        }
        with pytest.raises(AssertionError, match="Geometry type must be `Point`"):
            geojson_point_feature_to_kili_point_annotation(point)


class TestKiliLineToGeojson:
    def test_kili_line_to_geojson_linestring(self):
        polyline = [{"x": 1.0, "y": 2.0}, {"x": 3.0, "y": 4.0}]
        result = kili_line_to_geojson_linestring(polyline)
        expected = {"type": "LineString", "coordinates": [[1.0, 2.0], [3.0, 4.0]]}
        assert result == expected

    def test_kili_line_annotation_to_geojson_linestring_feature(self):
        polyline_annotation = {
            "children": {},
            "polyline": [{"x": -79.0, "y": -3.0}, {"x": -79.0, "y": -3.0}],
            "categories": [{"name": "A"}],
            "mid": "mid_object",
            "type": "polyline",
        }
        result = kili_line_annotation_to_geojson_linestring_feature(polyline_annotation, "job_name")
        expected = {
            "type": "Feature",
            "geometry": {"type": "LineString", "coordinates": [[-79.0, -3.0], [-79.0, -3.0]]},
            "id": "mid_object",
            "properties": {
                "kili": {
                    "categories": [{"name": "A"}],
                    "children": {},
                    "type": "polyline",
                    "job": "job_name",
                }
            },
        }
        assert result == expected

    def test_kili_line_annotation_wrong_type_raises_error(self):
        polyline_annotation = {
            "children": {},
            "polyline": [{"x": -79.0, "y": -3.0}],
            "categories": [{"name": "A"}],
            "type": "polygon",
        }
        with pytest.raises(AssertionError, match="Annotation type must be `polyline`"):
            kili_line_annotation_to_geojson_linestring_feature(polyline_annotation)


class TestGeojsonLineToKili:
    def test_geojson_linestring_feature_to_kili_line_annotation(self):
        line = {
            "type": "Feature",
            "geometry": {"type": "LineString", "coordinates": [[-79.0, -3.0], [-79.0, -3.0]]},
            "id": "mid_object",
            "properties": {
                "kili": {"categories": [{"name": "A"}], "children": {}, "job": "job_name"}
            },
        }
        result = geojson_linestring_feature_to_kili_line_annotation(line)
        expected = {
            "children": {},
            "polyline": [{"x": -79.0, "y": -3.0}, {"x": -79.0, "y": -3.0}],
            "categories": [{"name": "A"}],
            "mid": "mid_object",
            "type": "polyline",
        }
        assert result == expected

    def test_geojson_linestring_feature_wrong_geometry_type_raises_error(self):
        line = {"type": "Feature", "geometry": {"type": "Point", "coordinates": [-79.0, -3.0]}}
        with pytest.raises(AssertionError, match="Geometry type must be `LineString`"):
            geojson_linestring_feature_to_kili_line_annotation(line)


class TestKiliBboxToGeojson:
    def test_kili_bbox_to_geojson_polygon(self):
        vertices = [
            {"x": 12.0, "y": 3.0},
            {"x": 12.0, "y": 4.0},
            {"x": 13.0, "y": 4.0},
            {"x": 13.0, "y": 3.0},
        ]
        result = kili_bbox_to_geojson_polygon(vertices)
        expected = {
            "type": "Polygon",
            "coordinates": [[[12.0, 3.0], [13.0, 3.0], [13.0, 4.0], [12.0, 4.0], [12.0, 3.0]]],
        }
        assert result == expected

    def test_kili_bbox_annotation_to_geojson_polygon_feature(self):
        bbox_annotation = {
            "children": {},
            "boundingPoly": [
                {
                    "normalizedVertices": [
                        {"x": -12.6, "y": 12.87},
                        {"x": -42.6, "y": 22.17},
                        {"x": -17.6, "y": -22.4},
                        {"x": 2.6, "y": -1.87},
                    ]
                }
            ],
            "categories": [{"name": "A"}],
            "mid": "mid_object",
            "type": "rectangle",
        }
        result = kili_bbox_annotation_to_geojson_polygon_feature(bbox_annotation, "job_name")
        expected = {
            "type": "Feature",
            "geometry": {
                "type": "Polygon",
                "coordinates": [
                    [[-12.6, 12.87], [2.6, -1.87], [-17.6, -22.4], [-42.6, 22.17], [-12.6, 12.87]]
                ],
            },
            "id": "mid_object",
            "properties": {
                "kili": {
                    "categories": [{"name": "A"}],
                    "children": {},
                    "type": "rectangle",
                    "job": "job_name",
                }
            },
        }
        assert result == expected

    def test_kili_bbox_annotation_wrong_type_raises_error(self):
        bbox_annotation = {"boundingPoly": [{"normalizedVertices": []}], "type": "polygon"}
        with pytest.raises(AssertionError, match="Annotation type must be `rectangle`"):
            kili_bbox_annotation_to_geojson_polygon_feature(bbox_annotation)


class TestGeojsonBboxToKili:
    def test_geojson_polygon_feature_to_kili_bbox_annotation(self):
        polygon = {
            "type": "Feature",
            "geometry": {
                "type": "Polygon",
                "coordinates": [
                    [[-12.6, 12.87], [-42.6, 22.17], [-17.6, -22.4], [2.6, -1.87], [-12.6, 12.87]]
                ],
            },
            "id": "mid_object",
            "properties": {
                "kili": {
                    "categories": [{"name": "A"}],
                    "children": {},
                    "type": "rectangle",
                    "job": "job_name",
                }
            },
        }
        result = geojson_polygon_feature_to_kili_bbox_annotation(polygon)
        expected = {
            "children": {},
            "boundingPoly": [
                {
                    "normalizedVertices": [
                        {"x": -12.6, "y": 12.87},
                        {"x": 2.6, "y": -1.87},
                        {"x": -17.6, "y": -22.4},
                        {"x": -42.6, "y": 22.17},
                    ]
                }
            ],
            "categories": [{"name": "A"}],
            "mid": "mid_object",
            "type": "rectangle",
        }
        assert result == expected


class TestKiliPolygonToGeojson:
    def test_kili_polygon_to_geojson_polygon(self):
        vertices = [
            {"x": 10.42, "y": 27.12},
            {"x": 1.53, "y": 14.57},
            {"x": 147.45, "y": 14.12},
            {"x": 14.23, "y": 0.23},
        ]
        result = kili_polygon_to_geojson_polygon(vertices)

        # Check that result is a valid polygon with closed coordinates
        assert result["type"] == "Polygon"
        assert len(result["coordinates"]) == 1
        coords = result["coordinates"][0]
        assert coords[0] == coords[-1]  # First and last point should be the same
        assert len(coords) == 5  # 4 vertices + 1 closing point

    def test_kili_polygon_annotation_to_geojson_polygon_feature(self):
        polygon_annotation = {
            "children": {},
            "boundingPoly": [
                {
                    "normalizedVertices": [
                        {"x": -79.0, "y": -3.0},
                        {"x": 0.0, "y": 0.0},
                        {"x": 1.0, "y": 1.0},
                    ]
                }
            ],
            "categories": [{"name": "A"}],
            "mid": "mid_object",
            "type": "polygon",
        }
        result = kili_polygon_annotation_to_geojson_polygon_feature(polygon_annotation, "job_name")

        assert result["type"] == "Feature"
        assert result["geometry"]["type"] == "Polygon"
        assert result["id"] == "mid_object"
        assert result["properties"]["kili"]["job"] == "job_name"

    def test_kili_polygon_annotation_wrong_type_raises_error(self):
        polygon_annotation = {"boundingPoly": [{"normalizedVertices": []}], "type": "rectangle"}
        with pytest.raises(AssertionError, match="Annotation type must be `polygon`"):
            kili_polygon_annotation_to_geojson_polygon_feature(polygon_annotation)

    def test_polygon_with_self_intersection_raises_error(self):
        # Create a self-intersecting polygon (figure-8 shape)
        vertices = [
            {"x": 0.0, "y": 0.0},
            {"x": 1.0, "y": 1.0},
            {"x": 1.0, "y": 0.0},
            {"x": 0.0, "y": 1.0},
        ]
        with pytest.raises(ConversionError, match="Polygon order could not be identified"):
            kili_polygon_to_geojson_polygon(vertices)


class TestGeojsonPolygonToKili:
    def test_geojson_polygon_feature_to_kili_polygon_annotation(self):
        polygon = {
            "type": "Feature",
            "geometry": {
                "type": "Polygon",
                "coordinates": [[[-79.0, -3.0], [0.0, 0.0], [1.0, 1.0], [-79.0, -3.0]]],
            },
            "id": "mid_object",
            "properties": {
                "kili": {
                    "categories": [{"name": "A"}],
                    "children": {},
                    "type": "polygon",
                    "job": "job_name",
                }
            },
        }
        result = geojson_polygon_feature_to_kili_polygon_annotation(polygon)
        expected = {
            "children": {},
            "boundingPoly": [
                {
                    "normalizedVertices": [
                        {"x": -79.0, "y": -3.0},
                        {"x": 0.0, "y": 0.0},
                        {"x": 1.0, "y": 1.0},
                    ]
                }
            ],
            "categories": [{"name": "A"}],
            "mid": "mid_object",
            "type": "polygon",
        }
        assert result == expected


class TestKiliSegmentationToGeojson:
    def test_kili_segmentation_to_geojson_geometry_single_polygon(self):
        bounding_poly = [
            [
                {"normalizedVertices": [{"x": 0, "y": 0}, {"x": 1, "y": 0}, {"x": 1, "y": 1}]},
                {
                    "normalizedVertices": [
                        {"x": 0.2, "y": 0.2},
                        {"x": 0.8, "y": 0.2},
                        {"x": 0.8, "y": 0.8},
                    ]
                },
            ]
        ]
        result = kili_segmentation_to_geojson_geometry(bounding_poly)
        expected = {
            "type": "Polygon",
            "coordinates": [
                [[0, 0], [1, 0], [1, 1], [0, 0]],
                [[0.2, 0.2], [0.8, 0.2], [0.8, 0.8], [0.2, 0.2]],
            ],
        }
        assert result == expected

    def test_kili_segmentation_to_geojson_geometry_multipolygon(self):
        bounding_poly = [
            [{"normalizedVertices": [{"x": 0, "y": 0}, {"x": 1, "y": 0}, {"x": 1, "y": 1}]}],
            [{"normalizedVertices": [{"x": 2, "y": 2}, {"x": 3, "y": 2}, {"x": 3, "y": 3}]}],
        ]
        result = kili_segmentation_to_geojson_geometry(bounding_poly)
        expected = {
            "type": "MultiPolygon",
            "coordinates": [[[[0, 0], [1, 0], [1, 1], [0, 0]]], [[[2, 2], [3, 2], [3, 3], [2, 2]]]],
        }
        assert result == expected

    def test_kili_segmentation_annotation_to_geojson_polygon_feature_single_polygon(self):
        segmentation_annotation = {
            "children": {},
            "boundingPoly": [
                [
                    {"normalizedVertices": [{"x": 0, "y": 0}, {"x": 1, "y": 0}, {"x": 1, "y": 1}]},
                    {
                        "normalizedVertices": [
                            {"x": 0.2, "y": 0.2},
                            {"x": 0.8, "y": 0.2},
                            {"x": 0.8, "y": 0.8},
                        ]
                    },
                ]
            ],
            "categories": [{"name": "building"}],
            "mid": "building_001",
            "type": "semantic",
        }
        result = kili_segmentation_annotation_to_geojson_polygon_feature(
            segmentation_annotation, "detection_job"
        )

        assert result["type"] == "Feature"
        assert result["geometry"]["type"] == "Polygon"
        assert result["id"] == "building_001"
        assert result["properties"]["kili"]["job"] == "detection_job"
        assert len(result["geometry"]["coordinates"]) == 2  # One exterior ring, one hole

    def test_kili_segmentation_annotation_to_geojson_polygon_feature_multipolygon(self):
        segmentation_annotation = {
            "children": {},
            "boundingPoly": [
                [{"normalizedVertices": [{"x": 0, "y": 0}, {"x": 1, "y": 0}, {"x": 1, "y": 1}]}],
                [{"normalizedVertices": [{"x": 2, "y": 2}, {"x": 3, "y": 2}, {"x": 3, "y": 3}]}],
            ],
            "categories": [{"name": "forest"}],
            "mid": "forest_001",
            "type": "semantic",
        }
        result = kili_segmentation_annotation_to_geojson_polygon_feature(
            segmentation_annotation, "detection_job"
        )

        assert result["type"] == "Feature"
        assert result["geometry"]["type"] == "MultiPolygon"
        assert result["id"] == "forest_001"
        assert len(result["geometry"]["coordinates"]) == 2  # Two separate polygons

    def test_kili_segmentation_annotation_wrong_type_raises_error(self):
        segmentation_annotation = {"boundingPoly": [], "type": "polygon"}
        with pytest.raises(AssertionError, match="Annotation type must be `semantic`"):
            kili_segmentation_annotation_to_geojson_polygon_feature(segmentation_annotation)


class TestGeojsonSegmentationToKili:
    def test_geojson_polygon_feature_to_kili_segmentation_annotation_polygon(self):
        polygon = {
            "type": "Feature",
            "geometry": {
                "type": "Polygon",
                "coordinates": [
                    [[0, 0], [1, 0], [1, 1], [0, 0]],
                    [[0.2, 0.2], [0.8, 0.2], [0.8, 0.8], [0.2, 0.2]],
                ],
            },
            "id": "building_001",
            "properties": {
                "kili": {
                    "categories": [{"name": "building"}],
                    "children": {},
                    "type": "semantic",
                    "job": "detection_job",
                }
            },
        }
        result = geojson_polygon_feature_to_kili_segmentation_annotation(polygon)
        expected = [
            {
                "boundingPoly": [
                    {"normalizedVertices": [{"x": 0, "y": 0}, {"x": 1, "y": 0}, {"x": 1, "y": 1}]},
                    {
                        "normalizedVertices": [
                            {"x": 0.2, "y": 0.2},
                            {"x": 0.8, "y": 0.2},
                            {"x": 0.8, "y": 0.8},
                        ]
                    },
                ],
                "categories": [{"name": "building"}],
                "children": {},
                "mid": "building_001",
                "type": "semantic",
            }
        ]
        assert result == expected

    def test_geojson_polygon_feature_to_kili_segmentation_annotation_multipolygon(self):
        multipolygon = {
            "type": "Feature",
            "geometry": {
                "type": "MultiPolygon",
                "coordinates": [
                    [[[0, 0], [1, 0], [1, 1], [0, 0]]],
                    [[[2, 2], [3, 2], [3, 3], [2, 2]]],
                ],
            },
            "id": "forest_001",
            "properties": {
                "kili": {"categories": [{"name": "forest"}], "children": {}, "type": "semantic"}
            },
        }
        result = geojson_polygon_feature_to_kili_segmentation_annotation(multipolygon)
        expected = [
            {
                "boundingPoly": [
                    {"normalizedVertices": [{"x": 0, "y": 0}, {"x": 1, "y": 0}, {"x": 1, "y": 1}]}
                ],
                "categories": [{"name": "forest"}],
                "children": {},
                "mid": "forest_001",
                "type": "semantic",
            },
            {
                "boundingPoly": [
                    {"normalizedVertices": [{"x": 2, "y": 2}, {"x": 3, "y": 2}, {"x": 3, "y": 3}]}
                ],
                "categories": [{"name": "forest"}],
                "children": {},
                "mid": "forest_001",
                "type": "semantic",
            },
        ]
        assert result == expected

    def test_geojson_unsupported_geometry_type_raises_error(self):
        feature = {"type": "Feature", "geometry": {"type": "Point", "coordinates": [0, 0]}}
        with pytest.raises(
            AssertionError, match="Geometry type must be `Polygon` or `MultiPolygon`"
        ):
            geojson_polygon_feature_to_kili_segmentation_annotation(feature)


class TestFeatureCollections:
    def test_features_to_feature_collection(self):
        features = [
            {
                "type": "Feature",
                "geometry": {"type": "Point", "coordinates": [-79.0, -3.0]},
                "id": "1",
            },
            {
                "type": "Feature",
                "geometry": {"type": "Point", "coordinates": [-79.0, -3.0]},
                "id": "2",
            },
        ]
        result = features_to_feature_collection(features)
        expected = {
            "type": "FeatureCollection",
            "features": [
                {
                    "type": "Feature",
                    "geometry": {"type": "Point", "coordinates": [-79.0, -3.0]},
                    "id": "1",
                },
                {
                    "type": "Feature",
                    "geometry": {"type": "Point", "coordinates": [-79.0, -3.0]},
                    "id": "2",
                },
            ],
        }
        assert result == expected

    def test_kili_json_response_to_feature_collection_point_annotations(self):
        json_response = {
            "POINT_JOB": {
                "annotations": [
                    {
                        "categories": [{"name": "A"}],
                        "point": {"x": 1.0, "y": 2.0},
                        "mid": "point_1",
                        "type": "marker",
                    }
                ]
            }
        }
        result = kili_json_response_to_feature_collection(json_response)

        assert result["type"] == "FeatureCollection"
        assert len(result["features"]) == 1
        assert result["features"][0]["geometry"]["type"] == "Point"
        assert result["features"][0]["properties"]["kili"]["job"] == "POINT_JOB"

    def test_kili_json_response_to_feature_collection_line_annotations(self):
        json_response = {
            "LINE_JOB": {
                "annotations": [
                    {
                        "categories": [{"name": "road"}],
                        "polyline": [{"x": 0.0, "y": 0.0}, {"x": 1.0, "y": 1.0}],
                        "mid": "line_1",
                        "type": "polyline",
                    }
                ]
            }
        }
        result = kili_json_response_to_feature_collection(json_response)

        assert result["type"] == "FeatureCollection"
        assert len(result["features"]) == 1
        assert result["features"][0]["geometry"]["type"] == "LineString"

    def test_kili_json_response_to_feature_collection_bbox_annotations(self):
        json_response = {
            "BBOX_JOB": {
                "annotations": [
                    {
                        "categories": [{"name": "car"}],
                        "boundingPoly": [
                            {
                                "normalizedVertices": [
                                    {"x": 0.0, "y": 0.0},
                                    {"x": 0.0, "y": 1.0},
                                    {"x": 1.0, "y": 1.0},
                                    {"x": 1.0, "y": 0.0},
                                ]
                            }
                        ],
                        "mid": "bbox_1",
                        "type": "rectangle",
                    }
                ]
            }
        }
        result = kili_json_response_to_feature_collection(json_response)

        assert result["type"] == "FeatureCollection"
        assert len(result["features"]) == 1
        assert result["features"][0]["geometry"]["type"] == "Polygon"

    def test_kili_json_response_to_feature_collection_polygon_annotations(self):
        json_response = {
            "POLYGON_JOB": {
                "annotations": [
                    {
                        "categories": [{"name": "building"}],
                        "boundingPoly": [
                            {
                                "normalizedVertices": [
                                    {"x": 0.0, "y": 0.0},
                                    {"x": 1.0, "y": 0.0},
                                    {"x": 1.0, "y": 1.0},
                                ]
                            }
                        ],
                        "mid": "polygon_1",
                        "type": "polygon",
                    }
                ]
            }
        }
        result = kili_json_response_to_feature_collection(json_response)

        assert result["type"] == "FeatureCollection"
        assert len(result["features"]) == 1
        assert result["features"][0]["geometry"]["type"] == "Polygon"

    def test_kili_json_response_to_feature_collection_semantic_annotations(self):
        json_response = {
            "SEMANTIC_JOB": {
                "annotations": [
                    {
                        "categories": [{"name": "forest"}],
                        "boundingPoly": [
                            [
                                {
                                    "normalizedVertices": [
                                        {"x": 0, "y": 0},
                                        {"x": 1, "y": 0},
                                        {"x": 1, "y": 1},
                                    ]
                                }
                            ],
                            [
                                {
                                    "normalizedVertices": [
                                        {"x": 2, "y": 2},
                                        {"x": 3, "y": 2},
                                        {"x": 3, "y": 3},
                                    ]
                                }
                            ],
                        ],
                        "mid": "semantic_1",
                        "type": "semantic",
                    }
                ]
            }
        }
        result = kili_json_response_to_feature_collection(json_response)

        assert result["type"] == "FeatureCollection"
        assert len(result["features"]) == 1
        assert result["features"][0]["geometry"]["type"] == "MultiPolygon"

    def test_kili_json_response_to_feature_collection_classification_annotations(self):
        json_response = {"CLASSIFICATION_JOB": {"categories": [{"name": "positive"}]}}
        result = kili_json_response_to_feature_collection(json_response)

        assert result["type"] == "FeatureCollection"
        assert len(result["features"]) == 1
        assert result["features"][0]["geometry"] is None
        assert result["features"][0]["properties"]["kili"]["categories"] == [{"name": "positive"}]

    def test_kili_json_response_to_feature_collection_transcription_annotations(self):
        json_response = {"TRANSCRIPTION_JOB": {"text": "Hello world"}}
        result = kili_json_response_to_feature_collection(json_response)

        assert result["type"] == "FeatureCollection"
        assert len(result["features"]) == 1
        assert result["features"][0]["geometry"] is None
        assert result["features"][0]["properties"]["kili"]["text"] == "Hello world"

    def test_kili_json_response_to_feature_collection_mixed_annotations(self):
        json_response = {
            "POINT_JOB": {
                "annotations": [
                    {
                        "categories": [{"name": "A"}],
                        "point": {"x": 1.0, "y": 2.0},
                        "mid": "point_1",
                        "type": "marker",
                    }
                ]
            },
            "CLASSIFICATION_JOB": {"categories": [{"name": "positive"}]},
            "TRANSCRIPTION_JOB": {"text": "Hello world"},
        }
        result = kili_json_response_to_feature_collection(json_response)

        assert result["type"] == "FeatureCollection"
        assert len(result["features"]) == 3

    def test_kili_json_response_to_feature_collection_unsupported_annotation_type(self):
        json_response = {
            "UNSUPPORTED_JOB": {
                "annotations": [{"categories": [{"name": "A"}], "type": "unsupported_type"}]
            }
        }
        with pytest.warns(UserWarning, match="Annotation tools"):
            result = kili_json_response_to_feature_collection(json_response)

        assert result["type"] == "FeatureCollection"
        assert len(result["features"]) == 0

    def test_geojson_feature_collection_to_kili_json_response(self):
        feature_collection = {
            "type": "FeatureCollection",
            "features": [
                {
                    "type": "Feature",
                    "geometry": {"type": "Point", "coordinates": [1.0, 2.0]},
                    "id": "point_1",
                    "properties": {
                        "kili": {
                            "categories": [{"name": "A"}],
                            "type": "marker",
                            "job": "POINT_DETECTION_JOB",
                        }
                    },
                }
            ],
        }
        result = geojson_feature_collection_to_kili_json_response(feature_collection)
        expected = {
            "POINT_DETECTION_JOB": {
                "annotations": [
                    {
                        "categories": [{"name": "A"}],
                        "type": "marker",
                        "point": {"x": 1.0, "y": 2.0},
                        "mid": "point_1",
                        "children": {},
                    }
                ]
            }
        }
        assert result == expected

    def test_geojson_feature_collection_to_kili_json_response_classification(self):
        feature_collection = {
            "type": "FeatureCollection",
            "features": [
                {
                    "type": "Feature",
                    "geometry": None,
                    "properties": {
                        "kili": {"categories": [{"name": "positive"}], "job": "CLASSIFICATION_JOB"}
                    },
                }
            ],
        }
        result = geojson_feature_collection_to_kili_json_response(feature_collection)
        expected = {"CLASSIFICATION_JOB": {"categories": [{"name": "positive"}]}}
        assert result == expected

    def test_geojson_feature_collection_to_kili_json_response_transcription(self):
        feature_collection = {
            "type": "FeatureCollection",
            "features": [
                {
                    "type": "Feature",
                    "geometry": None,
                    "properties": {"kili": {"text": "Hello world", "job": "TRANSCRIPTION_JOB"}},
                }
            ],
        }
        result = geojson_feature_collection_to_kili_json_response(feature_collection)
        expected = {"TRANSCRIPTION_JOB": {"text": "Hello world"}}
        assert result == expected

    def test_geojson_feature_collection_wrong_type_raises_error(self):
        feature_collection = {"type": "NotFeatureCollection", "features": []}
        with pytest.raises(
            AssertionError, match="Feature collection type must be `FeatureCollection`"
        ):
            geojson_feature_collection_to_kili_json_response(feature_collection)

    def test_geojson_feature_collection_missing_job_raises_error(self):
        feature_collection = {
            "type": "FeatureCollection",
            "features": [
                {
                    "type": "Feature",
                    "geometry": {"type": "Point", "coordinates": [1.0, 2.0]},
                    "properties": {"kili": {"categories": [{"name": "A"}], "type": "marker"}},
                }
            ],
        }
        with pytest.raises(ValueError, match="Job name is missing"):
            geojson_feature_collection_to_kili_json_response(feature_collection)

    def test_geojson_feature_collection_missing_type_raises_error(self):
        feature_collection = {
            "type": "FeatureCollection",
            "features": [
                {
                    "type": "Feature",
                    "geometry": {"type": "Point", "coordinates": [1.0, 2.0]},
                    "properties": {"kili": {"categories": [{"name": "A"}], "job": "POINT_JOB"}},
                }
            ],
        }
        with pytest.raises(ValueError, match="Annotation `type` is missing"):
            geojson_feature_collection_to_kili_json_response(feature_collection)

    def test_geojson_feature_collection_unsupported_type_raises_error(self):
        feature_collection = {
            "type": "FeatureCollection",
            "features": [
                {
                    "type": "Feature",
                    "geometry": {"type": "Point", "coordinates": [1.0, 2.0]},
                    "properties": {
                        "kili": {
                            "categories": [{"name": "A"}],
                            "type": "unsupported",
                            "job": "POINT_JOB",
                        }
                    },
                }
            ],
        }
        with pytest.raises(ValueError, match="Annotation tool unsupported is not supported"):
            geojson_feature_collection_to_kili_json_response(feature_collection)

    def test_geojson_feature_collection_invalid_non_localised_feature_raises_error(self):
        feature_collection = {
            "type": "FeatureCollection",
            "features": [
                {
                    "type": "Feature",
                    "geometry": None,
                    "properties": {"kili": {"job": "INVALID_JOB"}},
                }
            ],
        }
        with pytest.raises(ValueError, match="Invalid kili property in non localised feature"):
            geojson_feature_collection_to_kili_json_response(feature_collection)


class TestConvertFromKiliToGeojsonFormat:
    def test_convert_from_kili_to_geojson_format(self):
        json_response = {
            "POINT_JOB": {
                "annotations": [
                    {
                        "categories": [{"name": "A"}],
                        "point": {"x": 1.0, "y": 2.0},
                        "mid": "point_1",
                        "type": "marker",
                    }
                ]
            }
        }
        result = convert_from_kili_to_geojson_format(json_response)

        assert result["type"] == "FeatureCollection"
        assert len(result["features"]) == 1
        assert result["features"][0]["geometry"]["type"] == "Point"
        assert result["features"][0]["properties"]["kili"]["job"] == "POINT_JOB"


class TestComplexScenarios:
    def test_complete_workflow_point_annotations(self):
        # Test complete round-trip: Kili -> GeoJSON -> Kili
        original_kili_response = {
            "POINT_JOB": {
                "annotations": [
                    {
                        "categories": [{"name": "landmark"}],
                        "point": {"x": -122.4194, "y": 37.7749},
                        "mid": "san_francisco",
                        "type": "marker",
                        "children": {},
                    }
                ]
            }
        }

        # Convert to GeoJSON
        geojson_result = kili_json_response_to_feature_collection(original_kili_response)

        # Convert back to Kili
        kili_result = geojson_feature_collection_to_kili_json_response(geojson_result)

        assert kili_result == original_kili_response

    def test_complete_workflow_mixed_annotations(self):
        # Test with multiple annotation types
        original_kili_response = {
            "POINT_JOB": {
                "annotations": [
                    {
                        "categories": [{"name": "landmark"}],
                        "point": {"x": -122.4194, "y": 37.7749},
                        "mid": "point_1",
                        "type": "marker",
                        "children": {},
                    }
                ]
            },
            "POLYGON_JOB": {
                "annotations": [
                    {
                        "categories": [{"name": "building"}],
                        "boundingPoly": [
                            {
                                "normalizedVertices": [
                                    {"x": 0.0, "y": 0.0},
                                    {"x": 1.0, "y": 0.0},
                                    {"x": 1.0, "y": 1.0},
                                ]
                            }
                        ],
                        "mid": "building_1",
                        "type": "polygon",
                        "children": {},
                    }
                ]
            },
            "CLASSIFICATION_JOB": {"categories": [{"name": "urban"}]},
        }

        # Convert to GeoJSON
        geojson_result = kili_json_response_to_feature_collection(original_kili_response)

        # Verify GeoJSON structure
        assert geojson_result["type"] == "FeatureCollection"
        assert len(geojson_result["features"]) == 3

        # Verify feature types
        feature_types = {
            f["geometry"]["type"] if f["geometry"] else None for f in geojson_result["features"]
        }
        assert feature_types == {"Point", "Polygon", None}

        # Convert back to Kili
        kili_result = geojson_feature_collection_to_kili_json_response(geojson_result)

        assert kili_result == original_kili_response

    def test_semantic_segmentation_multipolygon_workflow(self):
        # Test complex semantic segmentation with multipolygon
        original_kili_response = {
            "SEMANTIC_JOB": {
                "annotations": [
                    {
                        "boundingPoly": [
                            {
                                "normalizedVertices": [
                                    {"x": 0.1, "y": 0.1},
                                    {"x": 0.3, "y": 0.1},
                                    {"x": 0.3, "y": 0.3},
                                ]
                            },
                            {
                                "normalizedVertices": [
                                    {"x": 0.15, "y": 0.15},
                                    {"x": 0.25, "y": 0.15},
                                    {"x": 0.25, "y": 0.25},
                                ]
                            },
                        ],
                        "categories": [{"name": "forest"}],
                        "children": {},
                        "mid": "forest_complex",
                        "type": "semantic",
                    },
                    {
                        "boundingPoly": [
                            {
                                "normalizedVertices": [
                                    {"x": 0.5, "y": 0.5},
                                    {"x": 0.7, "y": 0.5},
                                    {"x": 0.7, "y": 0.7},
                                ]
                            }
                        ],
                        "categories": [{"name": "forest"}],
                        "children": {},
                        "mid": "forest_complex",
                        "type": "semantic",
                    },
                ]
            }
        }

        # Convert to GeoJSON
        geojson_result = kili_json_response_to_feature_collection(original_kili_response)

        # Verify it's a MultiPolygon
        assert geojson_result["features"][0]["geometry"]["type"] == "MultiPolygon"
        assert (
            len(geojson_result["features"][0]["geometry"]["coordinates"]) == 2
        )  # Two polygon groups
        assert (
            len(geojson_result["features"][0]["geometry"]["coordinates"][0]) == 2
        )  # First polygon has a hole
        assert (
            len(geojson_result["features"][0]["geometry"]["coordinates"][1]) == 1
        )  # Second polygon has no hole

        # Convert back to Kili
        kili_result = geojson_feature_collection_to_kili_json_response(geojson_result)

        assert kili_result == original_kili_response
