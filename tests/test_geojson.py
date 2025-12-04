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
                    [
                        {
                            "normalizedVertices": [
                                {"x": 0, "y": 0},
                                {"x": 1, "y": 0},
                                {"x": 1, "y": 1},
                            ]
                        },
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
                "categories": [{"name": "forest"}],
                "children": {},
                "mid": "forest_001",
                "type": "semantic",
            }
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
                            [
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
                            [
                                {
                                    "normalizedVertices": [
                                        {"x": 0.5, "y": 0.5},
                                        {"x": 0.7, "y": 0.5},
                                        {"x": 0.7, "y": 0.7},
                                    ]
                                }
                            ],
                        ],
                        "categories": [{"name": "forest"}],
                        "children": {},
                        "mid": "forest_complex",
                        "type": "semantic",
                    }
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

    def test_geojson_multipolygon_feature(self):
        """Test that all parts of a MultiPolygon get the same mid."""
        multipolygon = {
            "type": "Feature",
            "geometry": {
                "type": "MultiPolygon",
                "coordinates": [
                    [[[0, 0], [1, 0], [1, 1], [0, 0]]],  # First polygon
                    [[[2, 2], [3, 2], [3, 3], [2, 2]]],  # Second polygon
                    [[[4, 4], [5, 4], [5, 5], [4, 4]]],  # Third polygon
                ],
            },
            "id": "forest_multipart_001",
            "properties": {
                "kili": {"categories": [{"name": "forest"}], "children": {}, "type": "semantic"}
            },
        }

        result = geojson_polygon_feature_to_kili_segmentation_annotation(multipolygon)

        # Should return 1 annotations with a boundingPoly containing 3 parts
        assert len(result) == 1
        annotation = result[0]
        assert annotation["type"] == "semantic"
        assert annotation["categories"] == [{"name": "forest"}]
        assert annotation["children"] == {}
        assert annotation["mid"] == "forest_multipart_001"
        assert len(annotation["boundingPoly"]) == 3

        # Check coordinates match the expected polygon part
        expected_coords = [
            [{"x": 0, "y": 0}, {"x": 1, "y": 0}, {"x": 1, "y": 1}],
            [{"x": 2, "y": 2}, {"x": 3, "y": 2}, {"x": 3, "y": 3}],
            [{"x": 4, "y": 4}, {"x": 5, "y": 4}, {"x": 5, "y": 5}],
        ]
        for i, poly in enumerate(annotation["boundingPoly"]):
            assert poly[0]["normalizedVertices"] == expected_coords[i]

    def test_geojson_multipolygon_feature_custom_mid_override(self):
        """Test that custom mid parameter overrides the feature id."""
        multipolygon = {
            "type": "Feature",
            "geometry": {
                "type": "MultiPolygon",
                "coordinates": [
                    [[[0, 0], [1, 0], [1, 1], [0, 0]]],
                    [[[2, 2], [3, 2], [3, 3], [2, 2]]],
                ],
            },
            "id": "original_id",
            "properties": {
                "kili": {"categories": [{"name": "water"}], "children": {}, "type": "semantic"}
            },
        }

        custom_mid = "custom_water_id_123"
        result = geojson_polygon_feature_to_kili_segmentation_annotation(
            multipolygon, mid=custom_mid
        )

        # Should return 1 annotation with the custom mid
        assert len(result) == 1
        annotation = result[0]
        assert annotation["mid"] == custom_mid
        assert annotation["mid"] != "original_id"


class TestMultiPointConversion:
    def test_geojson_multipoint_feature_to_kili_point_annotations(self):
        from kili_formats.format.geojson import (
            geojson_multipoint_feature_to_kili_point_annotations,
        )

        multipoint = {
            "type": "Feature",
            "geometry": {"type": "MultiPoint", "coordinates": [[1.0, 2.0], [3.0, 4.0], [5.0, 6.0]]},
            "id": "stations_001",
            "properties": {
                "kili": {"categories": [{"name": "station"}], "children": {}, "type": "marker"}
            },
        }
        result = geojson_multipoint_feature_to_kili_point_annotations(multipoint)

        assert len(result) == 3
        for i, annotation in enumerate(result):
            assert annotation["type"] == "marker"
            assert annotation["categories"] == [{"name": "station"}]
            assert annotation["point"]["x"] == multipoint["geometry"]["coordinates"][i][0]
            assert annotation["point"]["y"] == multipoint["geometry"]["coordinates"][i][1]


class TestMultiLineStringConversion:
    def test_geojson_multilinestring_feature_to_kili_line_annotations(self):
        from kili_formats.format.geojson import (
            geojson_multilinestring_feature_to_kili_line_annotations,
        )

        multilinestring = {
            "type": "Feature",
            "geometry": {
                "type": "MultiLineString",
                "coordinates": [[[1.0, 2.0], [3.0, 4.0]], [[5.0, 6.0], [7.0, 8.0]]],
            },
            "id": "metro_lines_001",
            "properties": {
                "kili": {"categories": [{"name": "metro_line"}], "children": {}, "type": "polyline"}
            },
        }
        result = geojson_multilinestring_feature_to_kili_line_annotations(multilinestring)

        assert len(result) == 2
        for i, annotation in enumerate(result):
            assert annotation["type"] == "polyline"
            assert annotation["categories"] == [{"name": "metro_line"}]
            assert len(annotation["polyline"]) == 2


class TestPropertyFlattening:
    """Tests for GIS-friendly property flattening feature."""

    def test_flatten_properties_basic(self):
        """Test basic property flattening with single-select classification."""
        json_interface = {
            "jobs": {
                "SEMANTIC_JOB": {
                    "content": {"categories": {"LAND": {"name": "Land"}}},
                    "instruction": "Land Type",
                    "mlTask": "OBJECT_DETECTION",
                },
                "CLASSIFICATION_JOB": {
                    "content": {"categories": {"CROP": {"name": "Crop"}}},
                    "instruction": "Type",
                    "mlTask": "CLASSIFICATION",
                },
            }
        }

        json_response = {
            "SEMANTIC_JOB": {
                "annotations": [
                    {
                        "type": "semantic",
                        "boundingPoly": [
                            [{"normalizedVertices": [{"x": 0, "y": 0}, {"x": 1, "y": 1}]}]
                        ],
                        "categories": [{"name": "LAND"}],
                        "mid": "land_001",
                        "children": {"CLASSIFICATION_JOB": {"categories": [{"name": "CROP"}]}},
                    }
                ]
            }
        }

        result = kili_json_response_to_feature_collection(
            json_response, json_interface, flatten_properties=True
        )

        assert result["type"] == "FeatureCollection"
        assert len(result["features"]) == 1

        properties = result["features"][0]["properties"]
        assert properties["class"] == "Land"
        assert properties["Type"] == "Crop"
        assert "kili" in properties  # Original kili object preserved

    def test_flatten_properties_with_export_name(self):
        """Test that exportName takes precedence over instruction."""
        json_interface = {
            "jobs": {
                "SEMANTIC_JOB": {
                    "content": {"categories": {"LAND": {"name": "Land"}}},
                    "instruction": "Land Type",
                    "mlTask": "OBJECT_DETECTION",
                },
                "CLASSIFICATION_JOB": {
                    "content": {"categories": {"CROP": {"name": "Crop"}}},
                    "instruction": "Type",
                    "exportName": "CropType",
                    "mlTask": "CLASSIFICATION",
                },
            }
        }

        json_response = {
            "SEMANTIC_JOB": {
                "annotations": [
                    {
                        "type": "semantic",
                        "boundingPoly": [
                            [{"normalizedVertices": [{"x": 0, "y": 0}, {"x": 1, "y": 1}]}]
                        ],
                        "categories": [{"name": "LAND"}],
                        "mid": "land_001",
                        "children": {"CLASSIFICATION_JOB": {"categories": [{"name": "CROP"}]}},
                    }
                ]
            }
        }

        result = kili_json_response_to_feature_collection(
            json_response, json_interface, flatten_properties=True
        )

        properties = result["features"][0]["properties"]
        assert properties["CropType"] == "Crop"  # Uses exportName, not instruction

    def test_flatten_properties_multiselect(self):
        """Test multi-select classifications create arrays."""
        json_interface = {
            "jobs": {
                "SEMANTIC_JOB": {
                    "content": {"categories": {"LAND": {"name": "Land"}}},
                    "instruction": "Land Type",
                    "mlTask": "OBJECT_DETECTION",
                },
                "CLASSIFICATION_JOB": {
                    "content": {
                        "categories": {
                            "CROP": {"name": "Crop"},
                            "VEGETATION": {"name": "Vegetation"},
                        },
                        "input": "checkbox",
                    },
                    "instruction": "Type",
                    "mlTask": "CLASSIFICATION",
                },
            }
        }

        json_response = {
            "SEMANTIC_JOB": {
                "annotations": [
                    {
                        "type": "semantic",
                        "boundingPoly": [
                            [{"normalizedVertices": [{"x": 0, "y": 0}, {"x": 1, "y": 1}]}]
                        ],
                        "categories": [{"name": "LAND"}],
                        "mid": "land_001",
                        "children": {
                            "CLASSIFICATION_JOB": {
                                "categories": [{"name": "CROP"}, {"name": "VEGETATION"}]
                            }
                        },
                    }
                ]
            }
        }

        result = kili_json_response_to_feature_collection(
            json_response, json_interface, flatten_properties=True
        )

        properties = result["features"][0]["properties"]
        assert isinstance(properties["Type"], list)
        assert set(properties["Type"]) == {"Crop", "Vegetation"}

    def test_flatten_properties_nested_dot_notation(self):
        """Test nested classifications use dot notation."""
        json_interface = {
            "jobs": {
                "SEMANTIC_JOB": {
                    "content": {"categories": {"LAND": {"name": "Land"}}},
                    "instruction": "Land Type",
                    "mlTask": "OBJECT_DETECTION",
                },
                "CLASSIFICATION_JOB": {
                    "content": {
                        "categories": {"CROP": {"name": "Crop"}},
                        "input": "checkbox",
                    },
                    "instruction": "Type",
                    "mlTask": "CLASSIFICATION",
                },
                "CLASSIFICATION_JOB_0": {
                    "content": {"categories": {"WHEAT": {"name": "Wheat"}}},
                    "instruction": "CropType",
                    "mlTask": "CLASSIFICATION",
                },
                "CLASSIFICATION_JOB_1": {
                    "content": {"categories": {"YES": {"name": "Yes"}}},
                    "instruction": "Irrigation",
                    "mlTask": "CLASSIFICATION",
                },
            }
        }

        json_response = {
            "SEMANTIC_JOB": {
                "annotations": [
                    {
                        "type": "semantic",
                        "boundingPoly": [
                            [{"normalizedVertices": [{"x": 0, "y": 0}, {"x": 1, "y": 1}]}]
                        ],
                        "categories": [{"name": "LAND"}],
                        "mid": "land_001",
                        "children": {
                            "CLASSIFICATION_JOB": {
                                "categories": [
                                    {
                                        "name": "CROP",
                                        "children": {
                                            "CLASSIFICATION_JOB_0": {
                                                "categories": [{"name": "WHEAT"}]
                                            },
                                            "CLASSIFICATION_JOB_1": {
                                                "categories": [{"name": "YES"}]
                                            },
                                        },
                                    }
                                ]
                            }
                        },
                    }
                ]
            }
        }

        result = kili_json_response_to_feature_collection(
            json_response, json_interface, flatten_properties=True
        )

        properties = result["features"][0]["properties"]
        assert properties["Type.Crop.CropType"] == "Wheat"
        assert properties["Type.Crop.Irrigation"] == "Yes"

    def test_flatten_properties_multiselect_with_nested(self):
        """Test multi-select with nested classifications for each option."""
        json_interface = {
            "jobs": {
                "SEMANTIC_JOB": {
                    "content": {"categories": {"LAND": {"name": "Land"}}},
                    "instruction": "Land Type",
                    "mlTask": "OBJECT_DETECTION",
                },
                "CLASSIFICATION_JOB": {
                    "content": {
                        "categories": {
                            "CROP": {"name": "Crop"},
                            "VEGETATION": {"name": "Vegetation"},
                        },
                        "input": "checkbox",
                    },
                    "instruction": "Type",
                    "mlTask": "CLASSIFICATION",
                },
                "CLASSIFICATION_JOB_0": {
                    "content": {"categories": {"WHEAT": {"name": "Wheat"}}},
                    "instruction": "CropType",
                    "mlTask": "CLASSIFICATION",
                },
                "CLASSIFICATION_JOB_1": {
                    "content": {"categories": {"PINE": {"name": "Pine"}}},
                    "instruction": "Species",
                    "mlTask": "CLASSIFICATION",
                },
            }
        }

        json_response = {
            "SEMANTIC_JOB": {
                "annotations": [
                    {
                        "type": "semantic",
                        "boundingPoly": [
                            [{"normalizedVertices": [{"x": 0, "y": 0}, {"x": 1, "y": 1}]}]
                        ],
                        "categories": [{"name": "LAND"}],
                        "mid": "land_001",
                        "children": {
                            "CLASSIFICATION_JOB": {
                                "categories": [
                                    {
                                        "name": "CROP",
                                        "children": {
                                            "CLASSIFICATION_JOB_0": {
                                                "categories": [{"name": "WHEAT"}]
                                            }
                                        },
                                    },
                                    {
                                        "name": "VEGETATION",
                                        "children": {
                                            "CLASSIFICATION_JOB_1": {
                                                "categories": [{"name": "PINE"}]
                                            }
                                        },
                                    },
                                ]
                            }
                        },
                    }
                ]
            }
        }

        result = kili_json_response_to_feature_collection(
            json_response, json_interface, flatten_properties=True
        )

        properties = result["features"][0]["properties"]
        assert properties["class"] == "Land"
        assert set(properties["Type"]) == {"Crop", "Vegetation"}
        assert properties["Type.Crop.CropType"] == "Wheat"
        assert properties["Type.Vegetation.Species"] == "Pine"

    def test_flatten_properties_without_json_interface(self):
        """Test that flattening still works without json_interface (uses job names)."""
        json_response = {
            "SEMANTIC_JOB": {
                "annotations": [
                    {
                        "type": "semantic",
                        "boundingPoly": [
                            [{"normalizedVertices": [{"x": 0, "y": 0}, {"x": 1, "y": 1}]}]
                        ],
                        "categories": [{"name": "LAND"}],
                        "mid": "land_001",
                        "children": {"CLASSIFICATION_JOB": {"categories": [{"name": "CROP"}]}},
                    }
                ]
            }
        }

        result = kili_json_response_to_feature_collection(
            json_response, json_interface=None, flatten_properties=True
        )

        properties = result["features"][0]["properties"]
        assert properties["class"] == "LAND"  # Uses category name directly
        assert properties["CLASSIFICATION_JOB"] == "CROP"  # Uses job name directly

    def test_flatten_properties_preserves_kili_object(self):
        """Test that original kili object is always preserved."""
        json_interface = {
            "jobs": {
                "SEMANTIC_JOB": {
                    "content": {"categories": {"LAND": {"name": "Land"}}},
                    "instruction": "Land Type",
                    "mlTask": "OBJECT_DETECTION",
                },
            }
        }

        json_response = {
            "SEMANTIC_JOB": {
                "annotations": [
                    {
                        "type": "semantic",
                        "boundingPoly": [
                            [{"normalizedVertices": [{"x": 0, "y": 0}, {"x": 1, "y": 1}]}]
                        ],
                        "categories": [{"name": "LAND"}],
                        "mid": "land_001",
                        "children": {},
                    }
                ]
            }
        }

        result = kili_json_response_to_feature_collection(
            json_response, json_interface, flatten_properties=True
        )

        properties = result["features"][0]["properties"]
        assert "kili" in properties
        assert properties["kili"]["type"] == "semantic"
        assert properties["kili"]["categories"] == [{"name": "LAND"}]
        assert properties["kili"]["job"] == "SEMANTIC_JOB"

    def test_flatten_properties_different_annotation_types(self):
        """Test flattening works with different annotation types (point, polygon, bbox, line)."""
        json_interface = {
            "jobs": {
                "POINT_JOB": {
                    "content": {"categories": {"LANDMARK": {"name": "Landmark"}}},
                    "instruction": "Landmark",
                    "mlTask": "OBJECT_DETECTION",
                },
            }
        }

        json_response = {
            "POINT_JOB": {
                "annotations": [
                    {
                        "type": "marker",
                        "point": {"x": 1.0, "y": 2.0},
                        "categories": [{"name": "LANDMARK"}],
                        "mid": "point_001",
                        "children": {},
                    }
                ]
            }
        }

        result = kili_json_response_to_feature_collection(
            json_response, json_interface, flatten_properties=True
        )

        properties = result["features"][0]["properties"]
        assert properties["class"] == "Landmark"
        assert "kili" in properties

    def test_no_flattening_by_default(self):
        """Test that flattening doesn't happen when flatten_properties=False."""
        json_interface = {
            "jobs": {
                "SEMANTIC_JOB": {
                    "content": {"categories": {"LAND": {"name": "Land"}}},
                    "instruction": "Land Type",
                    "mlTask": "OBJECT_DETECTION",
                },
            }
        }

        json_response = {
            "SEMANTIC_JOB": {
                "annotations": [
                    {
                        "type": "semantic",
                        "boundingPoly": [
                            [{"normalizedVertices": [{"x": 0, "y": 0}, {"x": 1, "y": 1}]}]
                        ],
                        "categories": [{"name": "LAND"}],
                        "mid": "land_001",
                        "children": {},
                    }
                ]
            }
        }

        result = kili_json_response_to_feature_collection(
            json_response, json_interface, flatten_properties=False
        )

        properties = result["features"][0]["properties"]
        assert "class" not in properties
        assert "kili" in properties
        # Original nested structure
        assert properties["kili"]["categories"] == [{"name": "LAND"}]

    def test_flatten_properties_classification_job(self):
        """Test flattening works for classification jobs (non-localized features)."""
        json_interface = {
            "jobs": {
                "CLASSIFICATION_JOB": {
                    "content": {
                        "categories": {
                            "A": {"name": "Category A"},
                            "B": {"name": "Category B"},
                        },
                        "input": "checkbox",
                    },
                    "instruction": "Type",
                    "mlTask": "CLASSIFICATION",
                },
                "SUB_CLASSIFICATION": {
                    "content": {
                        "categories": {
                            "A1": {"name": "Sub A1"},
                        },
                        "input": "radio",
                    },
                    "instruction": "Subtype",
                    "mlTask": "CLASSIFICATION",
                },
            }
        }

        json_response = {
            "CLASSIFICATION_JOB": {
                "categories": [
                    {
                        "name": "A",
                        "children": {"SUB_CLASSIFICATION": {"categories": [{"name": "A1"}]}},
                    },
                    {"name": "B"},
                ]
            }
        }

        result = kili_json_response_to_feature_collection(
            json_response, json_interface, flatten_properties=True
        )

        assert result["type"] == "FeatureCollection"
        assert len(result["features"]) == 1

        properties = result["features"][0]["properties"]
        assert properties["class"] == "Category A"
        assert set(properties["Type"]) == {"Category A", "Category B"}
        assert properties["Type.Category A.Subtype"] == "Sub A1"
        assert "kili" in properties

    def test_round_trip_with_flattened_properties(self):
        """Test that features with flattened properties can be converted back to Kili format."""
        json_interface = {
            "jobs": {
                "SEMANTIC_JOB": {
                    "content": {"categories": {"LAND": {"name": "Land"}}},
                    "instruction": "Land Type",
                    "mlTask": "OBJECT_DETECTION",
                },
                "CLASSIFICATION_JOB": {
                    "content": {"categories": {"CROP": {"name": "Crop"}}},
                    "instruction": "Type",
                    "mlTask": "CLASSIFICATION",
                },
            }
        }

        original_response = {
            "SEMANTIC_JOB": {
                "annotations": [
                    {
                        "type": "semantic",
                        "boundingPoly": [
                            [{"normalizedVertices": [{"x": 0, "y": 0}, {"x": 1, "y": 1}]}]
                        ],
                        "categories": [{"name": "LAND"}],
                        "mid": "land_001",
                        "children": {"CLASSIFICATION_JOB": {"categories": [{"name": "CROP"}]}},
                    }
                ]
            }
        }

        # Convert to GeoJSON with flattening
        geojson_result = kili_json_response_to_feature_collection(
            original_response, json_interface, flatten_properties=True
        )

        # Convert back to Kili (should use the preserved kili object)
        kili_result = geojson_feature_collection_to_kili_json_response(geojson_result)

        # Check essential properties (boundingPoly format may differ between hierarchical/flat)
        assert len(kili_result["SEMANTIC_JOB"]["annotations"]) == 1
        result_ann = kili_result["SEMANTIC_JOB"]["annotations"][0]
        original_ann = original_response["SEMANTIC_JOB"]["annotations"][0]

        assert result_ann["type"] == original_ann["type"]
        assert result_ann["categories"] == original_ann["categories"]
        assert result_ann["mid"] == original_ann["mid"]
        assert result_ann["children"] == original_ann["children"]
        # Verify geometry is preserved (coordinates may be in different nesting levels)
        assert len(result_ann["boundingPoly"]) > 0

    def test_flatten_properties_with_transcription_subjob(self):
        """Test that transcription subjobs (children of annotations) are flattened."""
        json_interface = {
            "jobs": {
                "OBJECT_DETECTION_JOB_0": {
                    "mlTask": "OBJECT_DETECTION",
                    "instruction": "Object Detection",
                    "content": {
                        "categories": {
                            "LAND": {"name": "Land", "children": ["TRANSCRIPTION_JOB"]},
                            "WATER": {"name": "Water", "children": []},
                        },
                        "input": "radio",
                    },
                },
                "TRANSCRIPTION_JOB": {
                    "mlTask": "TRANSCRIPTION",
                    "instruction": "Description",
                    "exportName": "Description",
                    "content": {"input": "textField"},
                },
            }
        }

        kili_response = {
            "OBJECT_DETECTION_JOB_0": {
                "annotations": [
                    {
                        "categories": [{"name": "LAND"}],
                        "children": {
                            "TRANSCRIPTION_JOB": {"text": "This is a land parcel description"}
                        },
                        "mid": "annotation-1",
                        "type": "polygon",
                        "boundingPoly": [
                            {
                                "normalizedVertices": [
                                    {"x": 0.1, "y": 0.1},
                                    {"x": 0.9, "y": 0.1},
                                    {"x": 0.9, "y": 0.9},
                                    {"x": 0.1, "y": 0.9},
                                ]
                            }
                        ],
                    }
                ]
            }
        }

        result = kili_json_response_to_feature_collection(
            kili_response, json_interface, flatten_properties=True
        )

        assert len(result["features"]) == 1
        feature = result["features"][0]

        # Check that the transcription subjob appears in flattened properties
        assert "Object Detection.Land.Description" in feature["properties"]
        assert feature["properties"]["Object Detection.Land.Description"] == (
            "This is a land parcel description"
        )

        # Check that the main category is still present
        assert feature["properties"]["class"] == "Land"
        assert feature["properties"]["Object Detection"] == "Land"

        # Verify the kili object is preserved
        assert "kili" in feature["properties"]
        assert "TRANSCRIPTION_JOB" in feature["properties"]["kili"]["children"]


class TestGeometryCollectionConversion:
    def test_geojson_geometrycollection_feature_to_kili_annotations(self):
        from kili_formats.format.geojson import (
            geojson_geometrycollection_feature_to_kili_annotations,
        )

        geometrycollection = {
            "type": "Feature",
            "geometry": {
                "type": "GeometryCollection",
                "geometries": [
                    {"type": "Point", "coordinates": [1.0, 2.0]},
                    {"type": "LineString", "coordinates": [[3.0, 4.0], [5.0, 6.0]]},
                    {
                        "type": "Polygon",
                        "coordinates": [
                            [[7.0, 8.0], [9.0, 8.0], [9.0, 10.0], [7.0, 10.0], [7.0, 8.0]]
                        ],
                    },
                ],
            },
            "id": "complex_001",
            "properties": {"kili": {"categories": [{"name": "complex"}], "children": {}}},
        }
        result = geojson_geometrycollection_feature_to_kili_annotations(geometrycollection)

        assert len(result) == 3

        assert result[0]["type"] == "marker"
        assert result[0]["point"] == {"x": 1.0, "y": 2.0}
        assert result[0]["mid"] == "complex_001"

        assert result[1]["type"] == "polyline"
        assert len(result[1]["polyline"]) == 2
        assert result[1]["mid"] == "complex_001"

        assert result[2]["type"] == "polygon"
        assert len(result[2]["boundingPoly"][0]["normalizedVertices"]) == 4
        assert result[2]["mid"] == "complex_001"

    def test_geometrycollection_with_type_filter(self):
        from kili_formats.format.geojson import (
            geojson_geometrycollection_feature_to_kili_annotations,
        )

        geometrycollection = {
            "type": "Feature",
            "geometry": {
                "type": "GeometryCollection",
                "geometries": [
                    {"type": "Point", "coordinates": [1.0, 2.0]},
                    {"type": "LineString", "coordinates": [[3.0, 4.0], [5.0, 6.0]]},
                    {
                        "type": "Polygon",
                        "coordinates": [[[7.0, 8.0], [9.0, 8.0], [9.0, 10.0], [7.0, 8.0]]],
                    },
                ],
            },
            "properties": {
                "kili": {"type": "marker", "categories": [{"name": "complex"}], "children": {}}
            },
        }
        result = geojson_geometrycollection_feature_to_kili_annotations(geometrycollection)

        assert len(result) == 1
        assert result[0]["type"] == "marker"
