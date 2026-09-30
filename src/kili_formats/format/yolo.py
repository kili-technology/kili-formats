from typing import Dict, List, Optional, Tuple

from kili_formats.tool.base import reverse_rotation_vertices
from kili_formats.types import JobCategory, JobTool, YoloTask

Point = Tuple[float, float]

_YOLO_TASKS = (None, "detect", "segment")


def convert_from_kili_to_yolo_format(
    job_id: str, label: Dict, category_ids: Dict[str, JobCategory], task: Optional[YoloTask] = None
) -> List[Tuple]:
    """Convert the annotations of a job in a label to YOLO lines, one tuple per line.

    Args:
        job_id: The job whose annotations are converted.
        label: The label, with its `jsonResponse`.
        category_ids: The YOLO class of each category, by `get_category_full_name`.
        task: What the lines are written for. `"detect"`: a `class x y w h` line per bounding box,
            other shapes left out. `"segment"`: a `class x1 y1 … xn yn` line per polygon, semantic
            part and bounding box (its four corners); a part's holes are joined to its outline by
            a zero-width bridge, so a filled outline leaves them empty, and a shape of fewer than
            3 points is left out. `None`, the default: bounding boxes as detect lines and polygons
            as segment lines, together, as before this option.

    Returns:
        The class index followed by the normalized coordinates, for each line.

    Raises:
        ValueError: `task` is none of `"detect"`, `"segment"` or `None`.
    """
    if task not in _YOLO_TASKS:
        raise ValueError(f"Unknown YOLO task {task!r}: use 'detect', 'segment' or None.")
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
        outline = _unrotated_ring(bounding_poly[0], rotation_val)
        tool = annotation["type"]

        ## /!\ this part was only in the SDK to be tested
        if tool == JobTool.RECTANGLE and task != "segment":
            x_s, y_s = [x for x, _ in outline], [y for _, y in outline]
            x_min, y_min = min(x_s), min(y_s)
            x_max, y_max = max(x_s), max(y_s)
            bbox_center_x, bbox_center_y = (x_min + x_max) / 2, (y_min + y_max) / 2
            bbox_width, bbox_height = x_max - x_min, y_max - y_min
            converted_annotations.append(
                (category_idx.id, bbox_center_x, bbox_center_y, bbox_width, bbox_height)
            )

        elif tool in {JobTool.POLYGON, JobTool.SEMANTIC, JobTool.RECTANGLE} and task != "detect":
            # <class-index> <x1> <y1> <x2> <y2> ... <xn> <yn>. A mask's parts are annotations of
            # their own; the rings after the first one of a part are its holes.
            ring = outline
            if task == "segment":
                for hole in bounding_poly[1:]:
                    if "normalizedVertices" in hole:
                        ring = _bridge_hole(ring, _unrotated_ring(hole, rotation_val))
                if len(ring) < 3:
                    continue
            converted_annotations.append((category_idx.id, *[c for point in ring for c in point]))

    return converted_annotations


def get_category_full_name(job_id, category_name):
    """Return a full name to identify uniquely a category."""
    return f"{job_id}__{category_name}"


def _unrotated_ring(bounding_poly_item: Dict, rotation: int) -> List[Point]:
    """The ring's normalized vertices, the asset's rotation undone."""
    vertices = reverse_rotation_vertices(bounding_poly_item["normalizedVertices"], rotation)
    return [(vertice["x"], vertice["y"]) for vertice in vertices]


def _signed_area(ring: List[Point]) -> float:
    """Twice the ring's signed area: its sign tells the ring's orientation."""
    return sum(x_1 * y_2 - x_2 * y_1 for (x_1, y_1), (x_2, y_2) in zip(ring, ring[1:] + ring[:1]))


def _bridge_hole(ring: List[Point], hole: List[Point]) -> List[Point]:
    """One ring that walks `ring`, crosses to `hole` at their closest vertices, walks the hole the
    other way round and comes back: the bridge has no width, and filling the result leaves the
    hole empty, whichever fill rule is used.
    """
    if len(hole) < 3:
        return ring
    if (_signed_area(ring) > 0) == (_signed_area(hole) > 0):
        hole = hole[::-1]
    i, j = min(
        ((i, j) for i in range(len(ring)) for j in range(len(hole))),
        key=lambda pair: (ring[pair[0]][0] - hole[pair[1]][0]) ** 2
        + (ring[pair[0]][1] - hole[pair[1]][1]) ** 2,
    )
    return ring[: i + 1] + hole[j:] + hole[:j] + [hole[j], ring[i]] + ring[i + 1 :]
