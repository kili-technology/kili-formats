"""Geojson collection module."""

import warnings
from collections import defaultdict
from typing import Any, Dict, Sequence

from .bbox import (
    geojson_polygon_feature_to_kili_bbox_annotation,
    kili_bbox_annotation_to_geojson_polygon_feature,
)
from .classification import (
    kili_classification_annotation_to_geojson_non_localised_feature,
)
from .exceptions import ConversionError
from .line import (
    geojson_linestring_feature_to_kili_line_annotation,
    kili_line_annotation_to_geojson_linestring_feature,
)
from .point import (
    geojson_point_feature_to_kili_point_annotation,
    kili_point_annotation_to_geojson_point_feature,
)
from .polygon import (
    geojson_polygon_feature_to_kili_polygon_annotation,
    kili_polygon_annotation_to_geojson_polygon_feature,
)
from .segmentation import (
    geojson_polygon_feature_to_kili_segmentation_annotation,
    kili_segmentation_annotation_to_geojson_polygon_feature,
)
from .transcription import (
    kili_transcription_annotation_to_geojson_non_localised_feature,
)


def features_to_feature_collection(
    features: Sequence[Dict],
) -> Dict[str, Any]:
    """Convert a list of features to a feature collection.

    Args:
        features: a list of Geojson features.

    Returns:
        A Geojson feature collection.

    !!! Example
        ```python
        >>> features = [
            {
                'type': 'Feature',
                'geometry': {
                    'type': 'Point',
                    'coordinates': [-79.0, -3.0]},
                    'id': '1',
                }
            },
            {
                'type': 'Feature',
                'geometry': {
                    'type': 'Point',
                    'coordinates': [-79.0, -3.0]},
                    'id': '2',
                }
            }
        ]
        >>> features_to_feature_collection(features)
        {
            'type': 'FeatureCollection',
            'features': [
                {
                    'type': 'Feature',
                    'geometry': {
                        'type': 'Point',
                        'coordinates': [-79.0, -3.0]},
                        'id': '1',
                    }
                },
                {
                    'type': 'Feature',
                    'geometry': {
                        'type': 'Point',
                        'coordinates': [-79.0, -3.0]},
                        'id': '2',
                    }
                }
            ]
        }
        ```
    """
    return {"type": "FeatureCollection", "features": list(features)}


def _group_semantic_annotations_by_mid(annotations) -> Dict[str, Any]:
    """Group semantic annotations by their mid (for multi-part polygons)."""
    grouped = defaultdict(list)
    for annotation in annotations:
        if annotation.get("type") == "semantic" and "mid" in annotation:
            grouped[annotation["mid"]].append(annotation)
        else:
            # For annotations without mid or non-semantic, treat as individual
            grouped[id(annotation)] = [annotation]  # Use object id as unique key
    return grouped


def _convert_flat_to_hierarchical_format(annotations_group) -> Dict[str, Any]:
    """Convert flat format annotations to hierarchical format.

    Args:
        annotations_group: List of semantic annotations with the same mid

    Returns:
        Single annotation with hierarchical boundingPoly structure
    """
    if len(annotations_group) == 1:
        # Single annotation - check if it's already hierarchical
        annotation = annotations_group[0]
        if _is_hierarchical_format(annotation["boundingPoly"]):
            return annotation
        else:
            # Convert flat to hierarchical
            new_ann = annotation.copy()
            new_ann["boundingPoly"] = [annotation["boundingPoly"]]
            return new_ann
    else:
        # Multiple annotations with same mid - merge them
        base_ann = annotations_group[0].copy()
        all_bounding_poly = []

        for annotation in annotations_group:
            if _is_hierarchical_format(annotation["boundingPoly"]):
                # Already hierarchical - add each polygon group
                all_bounding_poly.extend(annotation["boundingPoly"])
            else:
                # Flat format - add as single polygon group
                all_bounding_poly.append(annotation["boundingPoly"])

        base_ann["boundingPoly"] = all_bounding_poly
        return base_ann


def _is_hierarchical_format(bounding_poly) -> bool:
    """Check if boundingPoly is in hierarchical format.

    Hierarchical: [ [ {normalizedVertices: [...]}, ... ], ... ]
    Flat: [ {normalizedVertices: [...]}, ... ]
    """
    if not bounding_poly or len(bounding_poly) == 0:
        return False

    first_element = bounding_poly[0]

    # If first element is a list, it's hierarchical
    if isinstance(first_element, list):
        return True

    # If first element is a dict with 'normalizedVertices', it's flat
    if isinstance(first_element, dict) and "normalizedVertices" in first_element:
        return False

    # Default to flat format
    return False


def kili_json_response_to_feature_collection(json_response: Dict[str, Any]) -> Dict[str, Any]:
    """Convert a Kili label json response to a Geojson feature collection.

    Args:
        json_response: a Kili label json response.

    Returns:
        A Geojson feature collection.

    !!! Example
        ```python
        >>> json_response = {
            'job_1': {
                'annotations': [...]
            },
            'job_2': {
                'annotations': [...]
            }
        }
        >>> kili_json_response_to_feature_collection(json_response)
        {
            'type': 'FeatureCollection',
            'features': [
                {
                    'type': 'Feature',
                    'geometry': {
                        ...
                    }
                },
                {
                    'type': 'Feature',
                    'geometry': {
                        ...
                    }
                }
            ]
        }
        ```
    """
    features = []

    annotation_tool_to_converter = {
        "rectangle": kili_bbox_annotation_to_geojson_polygon_feature,  # bbox
        "marker": kili_point_annotation_to_geojson_point_feature,  # point
        "polygon": kili_polygon_annotation_to_geojson_polygon_feature,  # polygon
        "polyline": kili_line_annotation_to_geojson_linestring_feature,  # line
        "semantic": kili_segmentation_annotation_to_geojson_polygon_feature,  # semantic
    }

    jobs_skipped = []
    ann_tools_not_supported = set()
    for job_name, job_response in json_response.items():
        if "text" in job_response:
            features.append(
                kili_transcription_annotation_to_geojson_non_localised_feature(
                    job_response, job_name
                ),
            )
            continue

        if "categories" in job_response:
            features.append(
                kili_classification_annotation_to_geojson_non_localised_feature(
                    job_response, job_name
                ),
            )
            continue

        if "annotations" not in job_response:
            jobs_skipped.append(job_name)
            continue

        # Group semantic annotations by mid before processing
        annotations = job_response["annotations"]
        semantic_annotations = [
            annotation for annotation in annotations if annotation.get("type") == "semantic"
        ]
        non_semantic_annotations = [
            annotation for annotation in annotations if annotation.get("type") != "semantic"
        ]

        # Process non-semantic annotations normally
        for annotation in non_semantic_annotations:
            annotation_tool = annotation.get("type")
            if annotation_tool not in annotation_tool_to_converter:
                ann_tools_not_supported.add(annotation_tool)
                continue

            converter = annotation_tool_to_converter[annotation_tool]

            try:
                feature = converter(annotation, job_name=job_name)
                features.append(feature)
            except ConversionError as error:
                warnings.warn(
                    error.args[0],
                    stacklevel=2,
                )
                continue

        # Process semantic annotations with grouping
        if semantic_annotations:
            grouped_semantic = _group_semantic_annotations_by_mid(semantic_annotations)

            for mid_or_id, annotations_group in grouped_semantic.items():
                try:
                    # Convert to hierarchical format if needed
                    merged_annotation = _convert_flat_to_hierarchical_format(annotations_group)

                    # Convert to GeoJSON
                    feature = kili_segmentation_annotation_to_geojson_polygon_feature(
                        merged_annotation, job_name=job_name
                    )
                    features.append(feature)
                except ConversionError as error:
                    warnings.warn(
                        error.args[0],
                        stacklevel=2,
                    )
                    continue
                except Exception as error:
                    warnings.warn(
                        f"Error converting semantic annotation: {error}",
                        stacklevel=2,
                    )
                    continue

    if jobs_skipped:
        warnings.warn(f"Jobs {jobs_skipped} cannot be exported to GeoJson format.", stacklevel=2)
    if ann_tools_not_supported:
        warnings.warn(
            f"Annotation tools {ann_tools_not_supported} are not supported and will be skipped.",
            stacklevel=2,
        )
    return features_to_feature_collection(features)


def geojson_feature_collection_to_kili_json_response(
    feature_collection: Dict[str, Any],
) -> Dict[str, Any]:
    """Convert a Geojson feature collection to a Kili label json response.

    Args:
        feature_collection: a Geojson feature collection.

    Returns:
        A Kili label json response.

    !!! Warning
        This method requires the `kili` key to be present in the geojson features' properties.
        In particular, the `kili` dictionary of a feature must contain the `categories` and `type` of the annotation.
        It must also contain the `job` name.

    !!! Example
        ```python
        >>> feature_collection = {
            'type': 'FeatureCollection',
            'features': [
                {
                    'type': 'Feature',
                    'geometry': {
                        ...
                    },
                    'properties': {
                        'kili': {
                            'categories': [{'name': 'A'}],
                            'type': 'marker',
                            'job': 'POINT_DETECTION_JOB'
                        }
                    }
                },
            ]
        }
        >>> geojson_feature_collection_to_kili_json_response(feature_collection)
        {
            'POINT_DETECTION_JOB': {
                'annotations': [
                    {
                        'categories': [{'name': 'A'}],
                        'type': 'marker',
                        'point': ...
                    }
                ]
            }
        }
        ```
    """
    assert (
        feature_collection["type"] == "FeatureCollection"
    ), f"Feature collection type must be `FeatureCollection`, got: {feature_collection['type']}"

    annotation_tool_to_converter = {
        "rectangle": geojson_polygon_feature_to_kili_bbox_annotation,
        "marker": geojson_point_feature_to_kili_point_annotation,
        "polygon": geojson_polygon_feature_to_kili_polygon_annotation,
        "polyline": geojson_linestring_feature_to_kili_line_annotation,
        "semantic": geojson_polygon_feature_to_kili_segmentation_annotation,
    }

    json_response = {}

    for feature in feature_collection["features"]:
        if feature.get("properties").get("kili", {}).get("job") is None:
            raise ValueError(f"Job name is missing in the GeoJson feature {feature}")

        job_name = feature["properties"]["kili"]["job"]

        if feature.get("geometry") is None:
            # non localised annotation
            if feature.get("properties").get("kili", {}).get("text") is not None:
                # transcription job
                json_response[job_name] = {"text": feature["properties"]["kili"]["text"]}
            elif feature.get("properties").get("kili", {}).get("categories") is not None:
                # classification job
                json_response[job_name] = {
                    "categories": feature["properties"]["kili"]["categories"]
                }
            else:
                raise ValueError("Invalid kili property in non localised feature")
            continue

        if feature.get("properties").get("kili", {}).get("type") is None:
            raise ValueError(f"Annotation `type` is missing in the GeoJson feature {feature}")

        annotation_tool = feature["properties"]["kili"]["type"]

        if annotation_tool not in annotation_tool_to_converter:
            raise ValueError(f"Annotation tool {annotation_tool} is not supported.")

        kili_annotation = annotation_tool_to_converter[annotation_tool](feature)

        if job_name not in json_response:
            json_response[job_name] = {}
        if "annotations" not in json_response[job_name]:
            json_response[job_name]["annotations"] = []

        if isinstance(kili_annotation, list):
            json_response[job_name]["annotations"].extend(kili_annotation)
        else:
            json_response[job_name]["annotations"].append(kili_annotation)

    return json_response
