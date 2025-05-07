from typing import Dict, List, Tuple

from kili_formats.tool.base import reverse_rotation_vertices
from kili_formats.types import JobCategory, JobTool

def convert_from_kili_to_yolo_format(
    job_id: str, label: Dict, category_ids: Dict[str, JobCategory]
) -> List[Tuple]:
    """Extract formatted annotations from labels and save the zip in the buckets."""
    if label is None or "jsonResponse" not in label:
        return []
    json_response = label["jsonResponse"]
    if not (job_id in json_response and "annotations" in json_response[job_id]):
        return []
    rotation_val = 0
    if "ROTATION_JOB" in json_response:
        rotation_val = json_response["ROTATION_JOB"]["rotation"]

    if not (job_id in json_response and "annotations" in json_response[job_id]):
        return []
    annotations = json_response[job_id]["annotations"]
    converted_annotations: List[Tuple] = []
    for annotation in annotations:
        category_idx: JobCategory = category_ids[
            get_category_full_name(job_id, annotation["categories"][0]["name"])
        ]
        if "boundingPoly" not in annotation:
            continue
        bounding_poly = annotation["boundingPoly"]
        if len(bounding_poly) < 1 or "normalizedVertices" not in bounding_poly[0]:
            continue
        normalized_vertices = bounding_poly[0]["normalizedVertices"]
        vertices_before_rotate = reverse_rotation_vertices(normalized_vertices, rotation_val)
        x_s: List[float] = [vertice["x"] for vertice in vertices_before_rotate]
        y_s: List[float] = [vertice["y"] for vertice in vertices_before_rotate]

        ## /!\ this part was only in the SDK to be tested
        if annotation["type"] == JobTool.RECTANGLE:
            x_min, y_min = min(x_s), min(y_s)
            x_max, y_max = max(x_s), max(y_s)
            bbox_center_x, bbox_center_y = (x_min + x_max) / 2, (y_min + y_max) / 2  # type: ignore
            bbox_width, bbox_height = x_max - x_min, y_max - y_min  # type: ignore
            converted_annotations.append(
                (category_idx.id, bbox_center_x, bbox_center_y, bbox_width, bbox_height)
            )

        elif annotation["type"] in {JobTool.POLYGON, JobTool.SEMANTIC}:
            # <class-index> <x1> <y1> <x2> <y2> ... <xn> <yn>
            # Each segmentation label must have a minimum of 3 xy points (polygon)
            points = [val for pair in zip(x_s, y_s) for val in pair]
            converted_annotations.append((category_idx.id, *points))

    return converted_annotations

def get_category_full_name(job_id, category_name):
    """Return a full name to identify uniquely a category."""
    return f"{job_id}__{category_name}"