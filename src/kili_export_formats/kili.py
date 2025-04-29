from typing import Callable, Dict, List

from .base import reverse_rotation_vertices
from .exceptions import NotCompatibleInputType, NotCompatibleOptions
from .types import ProjectDict


def clean_json_response(asset: Dict):
    if asset.get("latestLabel", {}) and asset["latestLabel"].get("jsonResponse", {}):
        if "ROTATION_JOB" in asset["latestLabel"]["jsonResponse"]:
            asset["latestLabel"]["jsonResponse"].pop("ROTATION_JOB")
    if asset.get("labels"):
        for label in asset["labels"]:
            if label.get("jsonResponse", {}) and "ROTATION_JOB" in label["jsonResponse"]:
                label["jsonResponse"].pop("ROTATION_JOB")

def format_json_response(label):
    """Format the label JSON response in the requested format."""
    keys = list(label["jsonResponse"].keys())

    for key in keys:
        if key.isdigit():
            label["jsonResponse"][int(key)] = label["jsonResponse"].pop(key)

def convert_to_pixel_coords(asset: Dict, project: ProjectDict, **kwargs) -> Dict:
    """Convert asset JSON response normalized vertices to pixel coordinates."""
    if asset.get("latestLabel", {}):
        _scale_label_vertices(asset["latestLabel"], asset, project, **kwargs)

    if asset.get("labels"):
        for label in asset["labels"]:
            _scale_label_vertices(label, asset, project, **kwargs)
    
    return asset

def _scale_label_vertices(label: Dict, asset: Dict,  project: ProjectDict, **kwargs) -> None:
    if not label.get("jsonResponse", {}):
        return

    is_label_rotated = (
        label["jsonResponse"]["ROTATION_JOB"]["rotation"] in [90, 270]
        if "ROTATION_JOB" in label["jsonResponse"]
        else False
    )

    rotation_val = 0
    if "ROTATION_JOB" in label["jsonResponse"]:
        rotation_val = label["jsonResponse"]["ROTATION_JOB"]["rotation"]

    normalized_vertices = kwargs.get("normalized_coordinates")

    if project["inputType"] == "PDF":
        _scale_json_response_vertices(
            json_resp=label["jsonResponse"],
            asset=asset,
            project=project,
            is_label_rotated=is_label_rotated,
            annotation_scaler=_scale_normalized_vertices_pdf_annotation,
        )

    elif project["inputType"] == "IMAGE":
        _scale_json_response_vertices(
            json_resp=label["jsonResponse"],
            asset=asset,
            project=project,
            rotation=rotation_val,
            normalized_vertices=normalized_vertices,
            annotation_scaler=_scale_normalized_vertices_image_video_annotation,
        )

    elif project["inputType"] == "VIDEO":
        for frame_resp in label["jsonResponse"].values():
            if frame_resp:
                _scale_json_response_vertices(
                    json_resp=frame_resp,
                    asset=asset,
                    project=project,
                    rotation=rotation_val,
                    normalized_vertices=normalized_vertices,
                    annotation_scaler=_scale_normalized_vertices_image_video_annotation,
                )

    else:
        raise NotCompatibleInputType(
            f"Labels of input type {project['inputType']} cannot be converted to pixel"
            " coordinates."
        )

def _scale_json_response_vertices(
        asset: Dict, project: ProjectDict, json_resp: Dict, annotation_scaler: Callable, **kwargs
) -> None:
    if not callable(annotation_scaler):
        return
    for job_name in json_resp:
        if _can_scale_vertices_for_job_name(job_name, project) and json_resp.get(job_name, {}).get(
            "annotations"
        ):
            for ann in json_resp[job_name]["annotations"]:
                annotation_scaler(ann, asset, **kwargs)

def _can_scale_vertices_for_job_name(job_name: str, project: ProjectDict) -> bool:
    if project["jsonInterface"] is None:
        raise Exception("No json interface found in project")
    return (
        # some old labels might not up to date with the json interface
        job_name in project["jsonInterface"]["jobs"]
        and (
            project["jsonInterface"]["jobs"][job_name]["mlTask"] == "OBJECT_DETECTION"
            or (
                project["inputType"] == "PDF"
                and project["jsonInterface"]["jobs"][job_name]["mlTask"]
                == "NAMED_ENTITIES_RECOGNITION"  # PDF NER jobs have vertices
            )
        )
    )

def _scale_vertex(vertex: Dict, width: int, height: int) -> Dict:
    return {"x": vertex["x"] * width, "y": vertex["y"] * height}
 
def _scale_all_vertices(object_, width: int, height: int):
    if isinstance(object_, List):
        return [_scale_all_vertices(obj, width=width, height=height) for obj in object_]

    if isinstance(object_, Dict):
        if sorted(object_.keys()) == ["x", "y"]:
            return _scale_vertex(object_, width=width, height=height)
        return {
            key: _scale_all_vertices(value, width=width, height=height)
            for key, value in object_.items()
        }
    return object_

    
def _scale_normalized_vertices_pdf_annotation(annotation: Dict, asset: Dict, **kwargs) -> None:
    """Scale normalized vertices of a PDF annotation.

    PDF annotations are different from image annotations because the asset width/height can vary.

    PDF only have BBox detection, so we only scale the boundingPoly and polys keys.
    """
    is_label_rotated = kwargs.get("is_label_rotated", False)

    if is_label_rotated:
        raise NotCompatibleOptions("PDF labels cannot be rotated")

    if "annotations" in annotation:
        # pdf annotations have two layers of "annotations"
        # https://docs.kili-technology.com/reference/export-object-entity-detection-and-relation#ner-in-pdfs
        for ann in annotation["annotations"]:
            _scale_normalized_vertices_pdf_annotation(ann, asset, **kwargs)

    # an annotation has three keys:
    # - pageNumberArray: list of page numbers
    # - polys: list of polygons
    # - boundingPoly: list of bounding polygons
    # each polygon is a dict with a key "normalizedVertices" that is a list of vertices
    if "polys" in annotation and "boundingPoly" in annotation:
        try:
            page_number_to_dimensions = {
                page_resolution["pageNumber"]: {
                    "width": page_resolution["width"],
                    "height": page_resolution["height"],
                }
                for page_resolution in asset["pageResolutions"]
            }
        except (KeyError, TypeError) as err:
            raise NotCompatibleOptions(
                "PDF labels export with absolute coordinates require `pageResolutions` in the"
                " asset. Please use `kili.update_properties_in_assets(page_resolutions_array=...)`"
                " to update the page resolutions of your asset.`"
            ) from err

        for key in ("polys", "boundingPoly"):
            annotation[key] = [
                {
                    **value,  # keep the original normalizedVertices
                    "vertices": _scale_all_vertices(
                        value["normalizedVertices"],
                        width=page_number_to_dimensions[page_number]["width"],
                        height=page_number_to_dimensions[page_number]["height"],
                    ),
                }
                for value, page_number in zip(annotation[key], annotation["pageNumberArray"])
            ]

def _scale_normalized_vertices_image_video_annotation(
    annotation: Dict, asset: Dict, **kwargs
) -> None:
    """Scale normalized vertices of an image/video object detection annotation."""
    try:
        width, height = get_asset_dimensions(asset)
    except (KeyError, TypeError):
        return
    
    rotation = kwargs.get("rotation", 0)
    normalized_vertices = kwargs.get("normalized_vertices", True)

    ## /!\ this was only in the SDK to be tested with application
    if not normalized_vertices and ("resolution" not in asset or asset["resolution"] is None):
        raise NotCompatibleOptions(
            "Image and video labels export with absolute coordinates require `resolution` in the"
            " asset. Please use `kili.update_properties_in_assets(resolution_array=...)` to update"
            " the resolution of your asset.`"
        )

    # bbox, segmentation, polygons
    if "boundingPoly" in annotation and normalized_vertices:
        annotation["boundingPoly"] = [
            {
                "normalizedVertices": reverse_rotation_vertices(
                    norm_vertices_dict["normalizedVertices"], rotation
                ),
            }
            for norm_vertices_dict in annotation["boundingPoly"]
        ]
        return

    if "boundingPoly" in annotation and not normalized_vertices:
        annotation["boundingPoly"] = [
            {
                "normalizedVertices": reverse_rotation_vertices(
                    norm_vertices_dict["normalizedVertices"], rotation
                ),
                "vertices": _scale_all_vertices(
                    reverse_rotation_vertices(norm_vertices_dict["normalizedVertices"], rotation),
                    width=width,
                    height=height,
                ),
            }
            for norm_vertices_dict in annotation["boundingPoly"]
        ]
    # point jobs
    if "point" in annotation:
        annotation["pointPixels"] = _scale_all_vertices(
            annotation["point"], width=width, height=height
        )

    # line, vector jobs
    if "polyline" in annotation:
        annotation["polylinePixels"] = _scale_all_vertices(
            annotation["polyline"], width=width, height=height
        )

    # pose estimation jobs
    if "points" in annotation:
        for point_dict in annotation["points"]:
            if "point" in point_dict:
                point_dict["pointPixels"] = _scale_all_vertices(
                    point_dict["point"], width=width, height=height
                )

def get_asset_dimensions(asset: Dict):
    """Returns the width and height of the asset."""
    resolution = asset["resolution"]
    return resolution["width"], resolution["height"]