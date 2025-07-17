"""Multi-linestring conversion functions between Kili and geojson formats."""

import uuid
from typing import Any, Dict, List, Optional


def geojson_multilinestring_feature_to_kili_line_annotations(
    multilinestring: Dict[str, Any],
    categories: Optional[List[Dict]] = None,
    children: Optional[Dict] = None,
) -> List[Dict[str, Any]]:
    """Convert a geojson multi-linestring feature to multiple Kili line annotations.

    Each linestring in the multi-linestring geometry is converted to a separate Kili polyline annotation.
    All resulting annotations share the same categories and children but have unique mids.

    Args:
        multilinestring: A geojson multi-linestring feature.
        categories: The categories of the annotations.
            If not provided, the categories are taken from the `kili` key of the geojson feature properties.
        children: The children of the annotations.
            If not provided, the children are taken from the `kili` key of the geojson feature properties.

    Returns:
        A list of Kili polyline annotations, one for each linestring in the multi-linestring.

    !!! Example
        ```python
        >>> multilinestring = {
            'type': 'Feature',
            'geometry': {
                'type': 'MultiLineString',
                'coordinates': [
                    [[1.0, 2.0], [3.0, 4.0]],
                    [[5.0, 6.0], [7.0, 8.0], [9.0, 10.0]]
                ]
            },
            'properties': {
                'kili': {
                    'categories': [{'name': 'road'}],
                    'children': {}
                }
            }
        }
        >>> geojson_multilinestring_feature_to_kili_line_annotations(multilinestring)
        [
            {
                'children': {},
                'categories': [{'name': 'road'}],
                'type': 'polyline',
                'polyline': [{'x': 1.0, 'y': 2.0}, {'x': 3.0, 'y': 4.0}],
                'mid': 'generated-uuid-1'
            },
            {
                'children': {},
                'categories': [{'name': 'road'}],
                'type': 'polyline',
                'polyline': [{'x': 5.0, 'y': 6.0}, {'x': 7.0, 'y': 8.0}, {'x': 9.0, 'y': 10.0}],
                'mid': 'generated-uuid-2'
            }
        ]
        ```
    """

    assert (
        multilinestring.get("type") == "Feature"
    ), f"Feature type must be `Feature`, got: {multilinestring['type']}"
    assert (
        multilinestring["geometry"]["type"] == "MultiLineString"
    ), f"Geometry type must be `MultiLineString`, got: {multilinestring['geometry']['type']}"

    children = children or multilinestring["properties"].get("kili", {}).get("children", {})
    categories = categories or multilinestring["properties"]["kili"]["categories"]

    coords = multilinestring["geometry"]["coordinates"]
    annotations = []

    for line_coords in coords:
        ret = {
            "children": children,
            "categories": categories,
            "type": "polyline",
            "polyline": [{"x": coord[0], "y": coord[1]} for coord in line_coords],
            "mid": str(uuid.uuid4()),
        }
        annotations.append(ret)

    return annotations
