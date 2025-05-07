from typing import Callable, Dict

from .tool.video import scale_normalized_vertices_image_video_annotation
from .tool.pdf import scale_normalized_vertices_pdf_annotation

from .exceptions import NotCompatibleInputType
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
            annotation_scaler=scale_normalized_vertices_pdf_annotation,
        )

    elif project["inputType"] == "IMAGE":
        _scale_json_response_vertices(
            json_resp=label["jsonResponse"],
            asset=asset,
            project=project,
            rotation=rotation_val,
            normalized_vertices=normalized_vertices,
            annotation_scaler=scale_normalized_vertices_image_video_annotation,
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
                    annotation_scaler=scale_normalized_vertices_image_video_annotation,
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
