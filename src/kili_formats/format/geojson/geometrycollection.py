"""Geometry collection conversion functions between Kili and geojson formats."""

import uuid
from typing import Any, Dict, List, Optional

from .line import geojson_linestring_feature_to_kili_line_annotation
from .multilinestring import geojson_multilinestring_feature_to_kili_line_annotations
from .multipoint import geojson_multipoint_feature_to_kili_point_annotations
from .point import geojson_point_feature_to_kili_point_annotation
from .polygon import geojson_polygon_feature_to_kili_polygon_annotation
from .segmentation import geojson_polygon_feature_to_kili_segmentation_annotation


def geojson_geometrycollection_feature_to_kili_annotations(
    geometrycollection: Dict[str, Any],
    categories: Optional[List[Dict]] = None,
    children: Optional[Dict] = None,
    mid: Optional[str] = None,
) -> List[Dict[str, Any]]:
    """Convert a geojson geometry collection feature to Kili annotations.

    Processes each geometry in the collection and converts it to the appropriate Kili annotation type.
    Points become marker annotations, LineStrings become polyline annotations,
    Polygons become polygon or semantic annotations depending on the type specified,
    MultiPoint and MultiLineString geometries are expanded into multiple annotations.

    Args:
        geometrycollection: A geojson geometry collection feature.
        categories: The categories of the annotations.
            If not provided, the categories are taken from the `kili` key of the geojson feature properties.
        children: The children of the annotations.
            If not provided, the children are taken from the `kili` key of the geojson feature properties.
        mid: The mid of the annotations.
            If not provided, the mid is taken from the `id` key of the geojson feature.
            If no id is available, a new UUID is generated.

    Returns:
        A list of Kili annotations corresponding to each geometry in the collection.

    !!! Example
        ```python
        >>> geometrycollection = {
            'type': 'Feature',
            'geometry': {
                'type': 'GeometryCollection',
                'geometries': [
                    {
                        'type': 'Point',
                        'coordinates': [1.0, 2.0]
                    },
                    {
                        'type': 'LineString',
                        'coordinates': [[3.0, 4.0], [5.0, 6.0]]
                    },
                    {
                        'type': 'Polygon',
                        'coordinates': [[[7.0, 8.0], [9.0, 8.0], [9.0, 10.0], [7.0, 10.0], [7.0, 8.0]]]
                    }
                ]
            },
            'id': 'complex_001',
            'properties': {
                'kili': {
                    'categories': [{'name': 'complex'}],
                    'children': {}
                }
            }
        }
        >>> geojson_geometrycollection_feature_to_kili_annotations(geometrycollection)
        [
            {
                'children': {},
                'point': {'x': 1.0, 'y': 2.0},
                'categories': [{'name': 'complex'}],
                'mid': 'complex_001',
                'type': 'marker'
            },
            {
                'children': {},
                'polyline': [{'x': 3.0, 'y': 4.0}, {'x': 5.0, 'y': 6.0}],
                'categories': [{'name': 'complex'}],
                'mid': 'complex_001',
                'type': 'polyline'
            },
            {
                'children': {},
                'boundingPoly': [{'normalizedVertices': [{'x': 7.0, 'y': 8.0}, {'x': 9.0, 'y': 8.0}, {'x': 9.0, 'y': 10.0}, {'x': 7.0, 'y': 10.0}]}],
                'categories': [{'name': 'complex'}],
                'mid': 'complex_001',
                'type': 'polygon'
            }
        ]
        ```
    """

    assert (
        geometrycollection.get("type") == "Feature"
    ), f"Feature type must be `Feature`, got: {geometrycollection['type']}"
    assert (
        geometrycollection["geometry"]["type"] == "GeometryCollection"
    ), f"Geometry type must be `GeometryCollection`, got: {geometrycollection['geometry']['type']}"

    children = children or geometrycollection["properties"].get("kili", {}).get("children", {})
    categories = categories or geometrycollection["properties"]["kili"]["categories"]

    kili_properties = geometrycollection["properties"].get("kili", {})
    annotation_type = kili_properties.get("type")

    annotation_mid = None
    if mid is not None:
        annotation_mid = str(mid)
    elif "id" in geometrycollection:
        annotation_mid = str(geometrycollection["id"])
    else:
        annotation_mid = str(uuid.uuid4())

    geometries = geometrycollection["geometry"]["geometries"]
    annotations = []

    for geometry in geometries:
        feature = {"type": "Feature", "geometry": geometry, "properties": {"kili": kili_properties}}

        if geometry["type"] == "Point":
            if annotation_type and annotation_type != "marker":
                continue
            ann = geojson_point_feature_to_kili_point_annotation(
                feature, categories=categories, children=children, mid=annotation_mid
            )
            annotations.append(ann)

        elif geometry["type"] == "LineString":
            if annotation_type and annotation_type != "polyline":
                continue
            ann = geojson_linestring_feature_to_kili_line_annotation(
                feature, categories=categories, children=children, mid=annotation_mid
            )
            annotations.append(ann)

        elif geometry["type"] == "Polygon":
            if annotation_type:
                if annotation_type == "polygon":
                    ann = geojson_polygon_feature_to_kili_polygon_annotation(
                        feature, categories=categories, children=children, mid=annotation_mid
                    )
                    annotations.append(ann)
                elif annotation_type == "semantic":
                    anns = geojson_polygon_feature_to_kili_segmentation_annotation(
                        feature, categories=categories, children=children, mid=annotation_mid
                    )
                    annotations.extend(anns)
            else:
                ann = geojson_polygon_feature_to_kili_polygon_annotation(
                    feature, categories=categories, children=children, mid=annotation_mid
                )
                annotations.append(ann)

        elif geometry["type"] == "MultiPoint":
            if annotation_type and annotation_type != "marker":
                continue
            anns = geojson_multipoint_feature_to_kili_point_annotations(
                feature, categories=categories, children=children
            )
            annotations.extend(anns)

        elif geometry["type"] == "MultiLineString":
            if annotation_type and annotation_type != "polyline":
                continue
            anns = geojson_multilinestring_feature_to_kili_line_annotations(
                feature, categories=categories, children=children
            )
            annotations.extend(anns)

        elif geometry["type"] == "MultiPolygon":
            if annotation_type and annotation_type != "semantic":
                continue
            anns = geojson_polygon_feature_to_kili_segmentation_annotation(
                feature, categories=categories, children=children, mid=annotation_mid
            )
            annotations.extend(anns)

    return annotations
