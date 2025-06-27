"""Geojson segmentation utilities."""

from typing import Any, Dict, List, Optional


def kili_segmentation_to_geojson_geometry(
    bounding_poly: List[List[Dict[str, List[Dict[str, Any]]]]]
) -> Dict[str, Any]:
    """Convert a Kili segmentation to a geojson polygon or multipolygon geometry.

    Args:
        bounding_poly: A Kili segmentation bounding polygon. List of polygon groups, each containing rings

    Returns:
        A geojson Polygon or MultiPolygon geometry.

    !!! Example
        ```python
        # Single polygon with holes (hierarchical structure)
        >>> bounding_poly = [
        ...     [  # First (and only) polygon group
        ...         {'normalizedVertices': [{'x': 0, 'y': 0}, {'x': 1, 'y': 0}, {'x': 1, 'y': 1}]},  # exterior
        ...         {'normalizedVertices': [{'x': 0.2, 'y': 0.2}, {'x': 0.8, 'y': 0.2}, {'x': 0.8, 'y': 0.8}]}  # hole
        ...     ]
        ... ]
        >>> kili_segmentation_to_geojson_geometry(bounding_poly)
        {
            'type': 'Polygon',
            'coordinates': [
                [[0, 0], [1, 0], [1, 1], [0, 0]],  # exterior ring (closed)
                [[0.2, 0.2], [0.8, 0.2], [0.8, 0.8], [0.2, 0.2]]  # hole (closed)
            ]
        }

        # MultiPolygon (hierarchical structure)
        >>> bounding_poly = [
        ...     [  # First polygon group
        ...         {'normalizedVertices': [{'x': 0, 'y': 0}, {'x': 1, 'y': 0}, {'x': 1, 'y': 1}]}
        ...     ],
        ...     [  # Second polygon group
        ...         {'normalizedVertices': [{'x': 2, 'y': 2}, {'x': 3, 'y': 2}, {'x': 3, 'y': 3}]}
        ...     ]
        ... ]
        >>> kili_segmentation_to_geojson_geometry(bounding_poly)
        {
            'type': 'MultiPolygon',
            'coordinates': [
                [[[0, 0], [1, 0], [1, 1], [0, 0]]],  # First polygon
                [[[2, 2], [3, 2], [3, 3], [2, 2]]]   # Second polygon
            ]
        }
        ```
    """
    # Determine Polygon vs MultiPolygon based on number of groups
    if len(bounding_poly) == 1:
        # Single polygon (potentially with holes)
        ret = {"type": "Polygon", "coordinates": []}
        for ring_dict in bounding_poly[0]:
            ring_coords = [[vertex["x"], vertex["y"]] for vertex in ring_dict["normalizedVertices"]]
            # Ensure the first and last points are identical (closed ring)
            if ring_coords[0] != ring_coords[-1]:
                ring_coords.append(ring_coords[0])
            ret["coordinates"].append(ring_coords)
        return ret
    else:
        # MultiPolygon
        ret = {"type": "MultiPolygon", "coordinates": []}
        for polygon_group in bounding_poly:
            polygon_coords = []
            for ring_dict in polygon_group:
                ring_coords = [
                    [vertex["x"], vertex["y"]] for vertex in ring_dict["normalizedVertices"]
                ]
                # Ensure the first and last points are identical (closed ring)
                if ring_coords[0] != ring_coords[-1]:
                    ring_coords.append(ring_coords[0])
                polygon_coords.append(ring_coords)
            ret["coordinates"].append(polygon_coords)
        return ret


def kili_segmentation_annotation_to_geojson_polygon_feature(
    segmentation_annotation: Dict[str, Any], job_name: Optional[str] = None
) -> Dict[str, Any]:
    """Convert a Kili segmentation annotation to a geojson polygon feature.

    Args:
        segmentation_annotation: A Kili segmentation annotation.
        job_name: The name of the job to which the annotation belongs.

    Returns:
        A geojson polygon feature (can be Polygon or MultiPolygon).

    !!! Example
        ```python
        # Simple polygon annotation
        >>> segmentation = {
        ...     'children': {},
        ...     'boundingPoly': [
        ...         [  # Single polygon group
        ...             {'normalizedVertices': [{'x': 0, 'y': 0}, {'x': 1, 'y': 0}, {'x': 1, 'y': 1}]},
        ...             {'normalizedVertices': [{'x': 0.2, 'y': 0.2}, {'x': 0.8, 'y': 0.2}, {'x': 0.8, 'y': 0.8}]}
        ...         ]
        ...     ],
        ...     'categories': [{'name': 'building'}],
        ...     'mid': 'building_001',
        ...     'type': 'semantic'
        ... }
        >>> kili_segmentation_annotation_to_geojson_polygon_feature(segmentation, 'detection_job')
        {
            'type': 'Feature',
            'geometry': {
                'type': 'Polygon',
                'coordinates': [
                    [[0, 0], [1, 0], [1, 1], [0, 0]],
                    [[0.2, 0.2], [0.8, 0.2], [0.8, 0.8], [0.2, 0.2]]
                ]
            },
            'id': 'building_001',
            'properties': {
                'kili': {
                    'categories': [{'name': 'building'}],
                    'children': {},
                    'type': 'semantic',
                    'job': 'detection_job'
                }
            }
        }

        # MultiPolygon annotation
        >>> segmentation = {
        ...     'children': {},
        ...     'boundingPoly': [
        ...         [{'normalizedVertices': [{'x': 0, 'y': 0}, {'x': 1, 'y': 0}, {'x': 1, 'y': 1}]}],  # First polygon
        ...         [{'normalizedVertices': [{'x': 2, 'y': 2}, {'x': 3, 'y': 2}, {'x': 3, 'y': 3}]}]   # Second polygon
        ...     ],
        ...     'categories': [{'name': 'forest'}],
        ...     'mid': 'forest_001',
        ...     'type': 'semantic'
        ... }
        >>> kili_segmentation_annotation_to_geojson_polygon_feature(segmentation, 'detection_job')
        {
            'type': 'Feature',
            'geometry': {
                'type': 'MultiPolygon',
                'coordinates': [
                    [[[0, 0], [1, 0], [1, 1], [0, 0]]],
                    [[[2, 2], [3, 2], [3, 3], [2, 2]]]
                ]
            },
            'id': 'forest_001',
            'properties': {
                'kili': {
                    'categories': [{'name': 'forest'}],
                    'children': {},
                    'type': 'semantic',
                    'job': 'detection_job'
                }
            }
        }
        ```
    """
    assert (
        segmentation_annotation["type"] == "semantic"
    ), f"Annotation type must be `semantic`, got: {segmentation_annotation['type']}"

    geometry = kili_segmentation_to_geojson_geometry(segmentation_annotation["boundingPoly"])

    ret = {
        "type": "Feature",
        "geometry": geometry,
    }

    if "mid" in segmentation_annotation:
        ret["id"] = segmentation_annotation["mid"]

    ret["properties"] = {
        "kili": {
            k: v for k, v in segmentation_annotation.items() if k not in ["mid", "boundingPoly"]
        }
    }

    if job_name is not None:
        ret["properties"]["kili"]["job"] = job_name

    return ret


def geojson_polygon_feature_to_kili_segmentation_annotation(
    polygon: Dict[str, Any],
    categories: Optional[List[Dict]] = None,
    children: Optional[Dict] = None,
    mid: Optional[str] = None,
) -> Dict[str, Any]:
    """Convert a geojson polygon feature to a Kili segmentation annotation.

    Supports both Polygon and MultiPolygon geometries.

    Args:
        polygon: A geojson polygon feature.
        categories: The categories of the annotation.
            If not provided, the categories are taken from the `kili` key of the geojson feature properties.
        children: The children of the annotation.
            If not provided, the children are taken from the `kili` key of the geojson feature properties.
        mid: The mid of the annotation.
            If not provided, the mid is taken from the `id` key of the geojson feature.

    Returns:
        A Kili segmentation annotation with hierarchical boundingPoly structure.

    !!! Example
        ```python
        # Polygon feature
        >>> polygon = {
        ...     'type': 'Feature',
        ...     'geometry': {
        ...         'type': 'Polygon',
        ...         'coordinates': [
        ...             [[0, 0], [1, 0], [1, 1], [0, 0]],  # exterior
        ...             [[0.2, 0.2], [0.8, 0.2], [0.8, 0.8], [0.2, 0.2]]  # hole
        ...         ]
        ...     },
        ...     'id': 'building_001',
        ...     'properties': {
        ...         'kili': {
        ...             'categories': [{'name': 'building'}],
        ...             'children': {},
        ...             'type': 'semantic',
        ...             'job': 'detection_job'
        ...         }
        ...     }
        ... }
        >>> geojson_polygon_feature_to_kili_segmentation_annotation(polygon)
        {
            'children': {},
            'boundingPoly': [
                [  # Single polygon group
                    {'normalizedVertices': [{'x': 0, 'y': 0}, {'x': 1, 'y': 0}, {'x': 1, 'y': 1}]},
                    {'normalizedVertices': [{'x': 0.2, 'y': 0.2}, {'x': 0.8, 'y': 0.2}, {'x': 0.8, 'y': 0.8}]}
                ]
            ],
            'categories': [{'name': 'building'}],
            'mid': 'building_001',
            'type': 'semantic'
        }

        # MultiPolygon feature
        >>> multipolygon = {
        ...     'type': 'Feature',
        ...     'geometry': {
        ...         'type': 'MultiPolygon',
        ...         'coordinates': [
        ...             [[[0, 0], [1, 0], [1, 1], [0, 0]]],  # First polygon
        ...             [[[2, 2], [3, 2], [3, 3], [2, 2]]]   # Second polygon
        ...         ]
        ...     },
        ...     'id': 'forest_001',
        ...     'properties': {
        ...         'kili': {
        ...             'categories': [{'name': 'forest'}],
        ...             'children': {},
        ...             'type': 'semantic'
        ...         }
        ...     }
        ... }
        >>> geojson_polygon_feature_to_kili_segmentation_annotation(multipolygon)
        {
            'children': {},
            'boundingPoly': [
                [{'normalizedVertices': [{'x': 0, 'y': 0}, {'x': 1, 'y': 0}, {'x': 1, 'y': 1}]}],
                [{'normalizedVertices': [{'x': 2, 'y': 2}, {'x': 3, 'y': 2}, {'x': 3, 'y': 3}]}]
            ],
            'categories': [{'name': 'forest'}],
            'mid': 'forest_001',
            'type': 'semantic'
        }
        ```
    """
    assert (
        polygon.get("type") == "Feature"
    ), f"Feature type must be `Feature`, got: {polygon['type']}"

    geometry_type = polygon["geometry"]["type"]
    assert geometry_type in [
        "Polygon",
        "MultiPolygon",
    ], f"Geometry type must be `Polygon` or `MultiPolygon`, got: {geometry_type}"

    children = children or polygon["properties"].get("kili", {}).get("children", {})
    categories = categories or polygon["properties"]["kili"]["categories"]

    ret = {
        "children": children,
        "categories": categories,
        "type": "semantic",
    }

    coords = polygon["geometry"]["coordinates"]

    if geometry_type == "Polygon":
        # Single polygon: wrap rings in a single group
        ret["boundingPoly"] = [
            [
                {"normalizedVertices": [{"x": coord[0], "y": coord[1]} for coord in ring[:-1]]}
                for ring in coords
            ]
        ]
    else:
        # MultiPolygon: each polygon becomes a separate group
        ret["boundingPoly"] = [
            [
                {"normalizedVertices": [{"x": coord[0], "y": coord[1]} for coord in ring[:-1]]}
                for ring in polygon_coords
            ]
            for polygon_coords in coords
        ]

    if mid is not None:
        ret["mid"] = str(mid)
    elif "id" in polygon:
        ret["mid"] = str(polygon["id"])

    return ret
