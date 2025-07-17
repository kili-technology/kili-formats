"""Multi-point conversion functions between Kili and geojson formats."""


import uuid
from typing import Any, Dict, List, Optional


def geojson_multipoint_feature_to_kili_point_annotations(
    multipoint: Dict[str, Any],
    categories: Optional[List[Dict]] = None,
    children: Optional[Dict] = None,
) -> List[Dict[str, Any]]:
    """Convert a geojson multi-point feature to multiple Kili point annotations.

    Each point in the multi-point geometry is converted to a separate Kili marker annotation.
    All resulting annotations share the same categories and children but have unique mids.

    Args:
        multipoint: A geojson multi-point feature.
        categories: The categories of the annotations.
            If not provided, the categories are taken from the `kili` key of the geojson feature properties.
        children: The children of the annotations.
            If not provided, the children are taken from the `kili` key of the geojson feature properties.

    Returns:
        A list of Kili marker annotations, one for each point in the multi-point.

    !!! Example
        ```python
        >>> multipoint = {
            'type': 'Feature',
            'geometry': {
                'type': 'MultiPoint',
                'coordinates': [[1.0, 2.0], [3.0, 4.0], [5.0, 6.0]]
            },
            'properties': {
                'kili': {
                    'categories': [{'name': 'landmark'}],
                    'children': {}
                }
            }
        }
        >>> geojson_multipoint_feature_to_kili_point_annotations(multipoint)
        [
            {
                'children': {},
                'categories': [{'name': 'landmark'}],
                'type': 'marker',
                'point': {'x': 1.0, 'y': 2.0},
                'mid': 'generated-uuid-1'
            },
            {
                'children': {},
                'categories': [{'name': 'landmark'}],
                'type': 'marker',
                'point': {'x': 3.0, 'y': 4.0},
                'mid': 'generated-uuid-2'
            },
            {
                'children': {},
                'categories': [{'name': 'landmark'}],
                'type': 'marker',
                'point': {'x': 5.0, 'y': 6.0},
                'mid': 'generated-uuid-3'
            }
        ]
        ```
    """

    assert (
        multipoint.get("type") == "Feature"
    ), f"Feature type must be `Feature`, got: {multipoint['type']}"
    assert (
        multipoint["geometry"]["type"] == "MultiPoint"
    ), f"Geometry type must be `MultiPoint`, got: {multipoint['geometry']['type']}"

    children = children or multipoint["properties"].get("kili", {}).get("children", {})
    categories = categories or multipoint["properties"]["kili"]["categories"]

    coords = multipoint["geometry"]["coordinates"]
    annotations = []

    for coord in coords:
        ret = {
            "children": children,
            "categories": categories,
            "type": "marker",
            "point": {"x": coord[0], "y": coord[1]},
            "mid": str(uuid.uuid4()),
        }
        annotations.append(ret)

    return annotations
