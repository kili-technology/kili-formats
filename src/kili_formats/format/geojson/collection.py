"""Geojson collection module."""

import warnings
from collections import defaultdict
from typing import Any, Dict, Optional, Sequence

from .bbox import (
    geojson_polygon_feature_to_kili_bbox_annotation,
    kili_bbox_annotation_to_geojson_polygon_feature,
)
from .classification import (
    kili_classification_annotation_to_geojson_non_localised_feature,
)
from .exceptions import ConversionError
from .geometrycollection import geojson_geometrycollection_feature_to_kili_annotations
from .line import (
    geojson_linestring_feature_to_kili_line_annotation,
    kili_line_annotation_to_geojson_linestring_feature,
)
from .multilinestring import geojson_multilinestring_feature_to_kili_line_annotations
from .multipoint import geojson_multipoint_feature_to_kili_point_annotations
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


def _get_job_friendly_name(json_interface: Optional[Dict[str, Any]], job_name: str) -> str:
    """Get friendly name for a job from json_interface.

    Args:
        json_interface: The project's json interface
        job_name: The job identifier (e.g., "CLASSIFICATION_JOB")

    Returns:
        The friendly name (from exportName or instruction) or the job_name if not found
    """
    if not json_interface or "jobs" not in json_interface:
        return job_name

    job = json_interface["jobs"].get(job_name)
    if not job:
        return job_name

    # Prefer exportName if available
    if "exportName" in job and job["exportName"]:
        return job["exportName"]

    # Fall back to instruction
    if "instruction" in job and job["instruction"]:
        return job["instruction"]

    return job_name


def _get_category_friendly_name(
    json_interface: Optional[Dict[str, Any]], job_name: str, category_name: str
) -> str:
    """Get friendly name for a category from json_interface.

    Args:
        json_interface: The project's json interface
        job_name: The job identifier
        category_name: The category identifier (e.g., "CROP")

    Returns:
        The friendly name from the category or the category_name if not found
    """
    if not json_interface or "jobs" not in json_interface:
        return category_name

    job = json_interface["jobs"].get(job_name)
    if not job or "content" not in job or "categories" not in job["content"]:
        return category_name

    category = job["content"]["categories"].get(category_name)
    if not category or "name" not in category:
        return category_name

    return category["name"]


def _is_multi_select_job(json_interface: Optional[Dict[str, Any]], job_name: str) -> bool:
    """Check if a job is multi-select (checkbox input).

    Args:
        json_interface: The project's json interface
        job_name: The job identifier

    Returns:
        True if the job uses checkbox input, False otherwise
    """
    if not json_interface or "jobs" not in json_interface:
        return False

    job = json_interface["jobs"].get(job_name)
    if not job or "content" not in job:
        return False

    return job["content"].get("input") == "checkbox"


def _is_child_of_category(
    json_interface: Optional[Dict[str, Any]],
    parent_job_name: str,
    category_name: str,
    child_job_name: str,
) -> bool:
    """Check if a child job is defined as a child of a specific category in json_interface.

    Args:
        json_interface: The project's json interface
        parent_job_name: The parent job identifier
        category_name: The category name
        child_job_name: The child job identifier to check

    Returns:
        True if the child job is listed in the category's children, False otherwise
    """
    if not json_interface or "jobs" not in json_interface:
        return False

    parent_job = json_interface["jobs"].get(parent_job_name)
    if not parent_job or "content" not in parent_job:
        return False

    categories = parent_job["content"].get("categories", {})
    category = categories.get(category_name)
    if not category:
        return False

    children = category.get("children", [])
    return child_job_name in children


def _flatten_classification_tree(
    children_dict: Dict[str, Any],
    json_interface: Optional[Dict[str, Any]],
    prefix: str = "",
) -> Dict[str, Any]:
    """Recursively flatten nested classification and transcription children into dot notation.

    Args:
        children_dict: The children dictionary from kili annotation
        json_interface: The project's json interface
        prefix: The current path prefix for nested properties

    Returns:
        A flat dictionary with dot-notated keys
    """
    flat_props = {}

    for child_job_name, child_data in children_dict.items():
        job_friendly_name = _get_job_friendly_name(json_interface, child_job_name)

        # Build the key with prefix
        key = f"{prefix}.{job_friendly_name}" if prefix else job_friendly_name

        # Handle transcription subjobs (with text field)
        if "text" in child_data:
            flat_props[key] = child_data["text"]
            continue

        # Handle classification subjobs (with categories field)
        if "categories" not in child_data:
            continue

        is_multi_select = _is_multi_select_job(json_interface, child_job_name)
        categories = child_data["categories"]

        if is_multi_select:
            # Multi-select: create array of friendly names
            friendly_categories = [
                _get_category_friendly_name(json_interface, child_job_name, cat.get("name", ""))
                for cat in categories
            ]
            flat_props[key] = friendly_categories

            # Process nested children for each category
            for cat in categories:
                if "children" in cat and cat["children"]:
                    cat_name = _get_category_friendly_name(
                        json_interface, child_job_name, cat.get("name", "")
                    )
                    nested_prefix = f"{key}.{cat_name}"
                    nested_props = _flatten_classification_tree(
                        cat["children"], json_interface, nested_prefix
                    )
                    flat_props.update(nested_props)
        else:
            # Single-select: use string value
            if len(categories) > 0:
                category_name = categories[0].get("name", "")
                friendly_name = _get_category_friendly_name(
                    json_interface, child_job_name, category_name
                )
                flat_props[key] = friendly_name

                # Process nested children
                if "children" in categories[0] and categories[0]["children"]:
                    nested_prefix = f"{key}.{friendly_name}"
                    nested_props = _flatten_classification_tree(
                        categories[0]["children"], json_interface, nested_prefix
                    )
                    flat_props.update(nested_props)

    return flat_props


def _flatten_properties_for_gis(
    kili_properties: Dict[str, Any],
    job_name: str,
    json_interface: Optional[Dict[str, Any]] = None,
) -> Dict[str, Any]:
    """Flatten Kili properties into GIS-friendly format.

    Args:
        kili_properties: The kili properties object from a feature
        job_name: The job name for this annotation
        json_interface: Optional json interface for friendly names

    Returns:
        A flattened properties dictionary with:
        - class: Main category display name
        - Friendly property names instead of job names
        - Nested classifications as dot notation
        - Multi-select as arrays
        - Original kili object preserved
    """
    flattened = {}

    # Check if this is a multi-select job
    is_multi_select = _is_multi_select_job(json_interface, job_name)
    job_friendly_name = _get_job_friendly_name(json_interface, job_name)

    # Set class attribute from main category
    if "categories" in kili_properties and kili_properties["categories"]:
        categories = kili_properties["categories"]

        # Get friendly names for all categories
        category_friendly_names = [
            _get_category_friendly_name(json_interface, job_name, cat.get("name", ""))
            for cat in categories
        ]

        # Set class from first category
        if category_friendly_names:
            flattened["class"] = category_friendly_names[0]

        # For root job, add a property with the job's friendly name
        if is_multi_select:
            # Multi-select: array of category names
            flattened[job_friendly_name] = category_friendly_names
        else:
            # Single-select: just the value
            if category_friendly_names:
                flattened[job_friendly_name] = category_friendly_names[0]

        # Process children for each category
        for i, cat in enumerate(categories):
            if "children" in cat and cat["children"]:
                cat_friendly_name = category_friendly_names[i]
                # Build prefix for nested properties
                prefix = f"{job_friendly_name}.{cat_friendly_name}"
                nested_props = _flatten_classification_tree(cat["children"], json_interface, prefix)
                flattened.update(nested_props)

    # Flatten children (subjobs like transcriptions or nested classifications)
    if "children" in kili_properties and kili_properties["children"]:
        # Determine if children belong to a category or are independent
        children_with_prefix = {}
        children_without_prefix = {}

        if "categories" in kili_properties and kili_properties["categories"]:
            # Check each child job to see if it belongs to the category
            categories = kili_properties["categories"]
            first_category_name = categories[0].get("name", "") if categories else ""

            for child_job_name, child_data in kili_properties["children"].items():
                # Check if this child is defined as a child of the first category
                if _is_child_of_category(
                    json_interface, job_name, first_category_name, child_job_name
                ):
                    children_with_prefix[child_job_name] = child_data
                else:
                    children_without_prefix[child_job_name] = child_data

            # Process children that belong to the category (with prefix)
            if children_with_prefix:
                category_friendly_names = [
                    _get_category_friendly_name(json_interface, job_name, cat.get("name", ""))
                    for cat in categories
                ]
                if category_friendly_names:
                    prefix = f"{job_friendly_name}.{category_friendly_names[0]}"
                    flat_children = _flatten_classification_tree(
                        children_with_prefix, json_interface, prefix
                    )
                    flattened.update(flat_children)

            # Process independent children (without prefix)
            if children_without_prefix:
                flat_children = _flatten_classification_tree(
                    children_without_prefix, json_interface
                )
                flattened.update(flat_children)
        else:
            # No categories, process all children without prefix
            flat_children = _flatten_classification_tree(
                kili_properties["children"], json_interface
            )
            flattened.update(flat_children)

    # Preserve original kili object
    flattened["kili"] = kili_properties

    return flattened


def kili_json_response_to_feature_collection(
    json_response: Dict[str, Any],
    json_interface: Optional[Dict[str, Any]] = None,
    flatten_properties: bool = False,
) -> Dict[str, Any]:
    """Convert a Kili label json response to a Geojson feature collection.

    Args:
        json_response: a Kili label json response.
        json_interface: Optional json interface for friendly property names.
        flatten_properties: If True, flatten properties for GIS-friendly format.

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
            feature = kili_transcription_annotation_to_geojson_non_localised_feature(
                job_response, job_name
            )

            # Flatten properties if requested (transcriptions typically don't have nested classifications)
            if flatten_properties and "properties" in feature and "kili" in feature["properties"]:
                feature["properties"] = _flatten_properties_for_gis(
                    feature["properties"]["kili"], job_name, json_interface
                )

            features.append(feature)
            continue

        if "categories" in job_response:
            feature = kili_classification_annotation_to_geojson_non_localised_feature(
                job_response, job_name
            )

            # Flatten properties if requested
            if flatten_properties and "properties" in feature and "kili" in feature["properties"]:
                feature["properties"] = _flatten_properties_for_gis(
                    feature["properties"]["kili"], job_name, json_interface
                )

            features.append(feature)
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

                if (
                    flatten_properties
                    and "properties" in feature
                    and "kili" in feature["properties"]
                ):
                    feature["properties"] = _flatten_properties_for_gis(
                        feature["properties"]["kili"], job_name, json_interface
                    )

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

                    if (
                        flatten_properties
                        and "properties" in feature
                        and "kili" in feature["properties"]
                    ):
                        feature["properties"] = _flatten_properties_for_gis(
                            feature["properties"]["kili"], job_name, json_interface
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

        geometry_type = feature["geometry"]["type"]

        if geometry_type == "GeometryCollection":
            kili_annotations = geojson_geometrycollection_feature_to_kili_annotations(feature)
        elif geometry_type == "MultiPoint":
            kili_annotations = geojson_multipoint_feature_to_kili_point_annotations(feature)
        elif geometry_type == "MultiLineString":
            kili_annotations = geojson_multilinestring_feature_to_kili_line_annotations(feature)
        else:
            if feature.get("properties").get("kili", {}).get("type") is None:
                raise ValueError(f"Annotation `type` is missing in the GeoJson feature {feature}")

            annotation_tool = feature["properties"]["kili"]["type"]

            if annotation_tool not in annotation_tool_to_converter:
                raise ValueError(f"Annotation tool {annotation_tool} is not supported.")

            kili_annotation = annotation_tool_to_converter[annotation_tool](feature)
            kili_annotations = (
                kili_annotation if isinstance(kili_annotation, list) else [kili_annotation]
            )

        if job_name not in json_response:
            json_response[job_name] = {}
        if "annotations" not in json_response[job_name]:
            json_response[job_name]["annotations"] = []

        json_response[job_name]["annotations"].extend(kili_annotations)

    return json_response
