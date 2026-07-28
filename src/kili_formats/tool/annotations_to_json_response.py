"""Annotation object to json response converter.

Only LLM projects rebuild their ``jsonResponse`` from annotations client-side.
All other project types (image, video, geospatial, audio, ...) are served the
backend-computed ``jsonResponse`` through ``jsonResponseUrl``, so the video,
object-detection and interpolation helpers that used to live here have been
removed (they now live in the backend ``UseCasesLabelJsonResponse``).
"""

from collections import defaultdict
from typing import Dict, List, Optional, cast

from kili_formats.types import (
    ClassicAnnotation,
    ClassificationAnnotation,
    ComparisonAnnotation,
    JobName,
    RankingAnnotation,
    TranscriptionAnnotation,
)


class AnnotationsToJsonResponseConverter:
    """Convert annotations to JSON response."""

    def __init__(self, project_input_type: str, json_interface) -> None:
        """Initialize the converter."""
        self._project_input_type = project_input_type
        self._project_json_interface = json_interface

    def _label_has_json_response_data(self, label: Dict) -> bool:
        job_names_in_json_resp = set(label["jsonResponse"].keys())
        return any(
            job_name in job_names_in_json_resp for job_name in self._project_json_interface["jobs"]
        )

    def patch_label_json_response(
        self,
        asset: Optional[Dict],
        label: Dict,
        annotations: List[ClassicAnnotation],
    ) -> None:
        """Patch the label json response using the annotations.

        Modifies the input label. Only LLM projects rebuild their ``jsonResponse``
        client-side; every other project type is served via ``jsonResponseUrl``.
        """
        if self._project_input_type in {
            "LLM_INSTR_FOLLOWING",
            "LLM_STATIC",
        }:
            if not annotations and self._label_has_json_response_data(label):
                return

            label["jsonResponse"] = _llm_annotations_to_json_response(annotations=annotations)


def _llm_annotations_to_json_response(
    annotations: List[ClassicAnnotation],
) -> Dict[JobName, Dict]:
    """Convert LLM label annotations to a json response."""
    json_resp = defaultdict(dict)

    for i, ann in enumerate(annotations):
        if ann["path"]:  # skip child annotations
            continue

        other_annotations = annotations[:i] + annotations[i + 1 :]

        if ann["__typename"] == "ClassificationAnnotation":
            ann = cast(ClassificationAnnotation, ann)
            ann_json_resp = _classification_annotation_to_json_response(ann, other_annotations)
            for job_name, job_resp in ann_json_resp.items():
                json_resp.setdefault(job_name, {}).setdefault("categories", []).extend(
                    job_resp["categories"]
                )

        elif ann["__typename"] == "ComparisonAnnotation":
            ann = cast(ComparisonAnnotation, ann)
            ann_json_resp = _comparison_annotation_to_json_response(ann)
            for job_name, job_resp in ann_json_resp.items():
                json_resp.setdefault(job_name, {}).setdefault("choice", job_resp["choice"])

        elif ann["__typename"] == "RankingAnnotation":
            ann = cast(RankingAnnotation, ann)
            ann_json_resp = _ranking_annotation_to_json_response(ann)
            for job_name, job_resp in ann_json_resp.items():
                json_resp.setdefault(job_name, {}).setdefault("orders", []).extend(
                    job_resp["orders"]
                )

        elif ann["__typename"] == "TranscriptionAnnotation":
            ann = cast(TranscriptionAnnotation, ann)
            ann_json_resp = _transcription_annotation_to_json_response(ann)
            for job_name, job_resp in ann_json_resp.items():
                json_resp.setdefault(job_name, {}).setdefault("text", job_resp["text"])

        else:
            raise NotImplementedError(f"Cannot convert annotation to json response: {ann}")

    return dict(json_resp)


def _comparison_annotation_to_json_response(
    annotation: ComparisonAnnotation,
) -> Dict[JobName, Dict]:
    """Convert comparison annotation to a json response."""
    json_resp = {
        annotation["job"]: {
            "choice": annotation["annotationValue"]["choice"],
        }
    }

    return json_resp


def _ranking_annotation_to_json_response(
    annotation: RankingAnnotation,
) -> Dict[JobName, Dict]:
    """Convert ranking annotation to a json response.

    Ranking jobs cannot have child jobs.
    """
    json_resp = {
        annotation["job"]: {
            "orders": sorted(
                annotation["annotationValue"]["orders"], key=lambda item: int(item["rank"])
            ),
        }
    }

    return json_resp


def _transcription_annotation_to_json_response(
    annotation: TranscriptionAnnotation,
) -> Dict[JobName, Dict]:
    """Convert transcription annotation to a json response.

    Transcription jobs cannot have child jobs.
    """
    json_resp = {
        annotation["job"]: {
            "text": annotation["annotationValue"]["text"],
        }
    }

    return json_resp


def _get_child_annotations(
    annotation: ClassicAnnotation, other_annotations: List[ClassicAnnotation]
) -> List[ClassicAnnotation]:
    """Get the child annotations (child jobs) of an annotation."""
    return [
        ann
        for ann in other_annotations
        # ann["path"] is a list of couples (annotationId, category)
        if len(ann["path"]) > 0
        and ann["path"][-1][0] == annotation["id"]
        and annotation["path"] == ann["path"][:-1]
    ]


def _compute_children_json_resp(
    child_annotations: List[ClassicAnnotation],
    other_annotations: List[ClassicAnnotation],
) -> Dict[JobName, Dict]:
    """Compute the json response of the child jobs of an annotation."""
    children_json_resp = defaultdict(dict)

    for child_ann in child_annotations:
        if child_ann["__typename"] == "ClassificationAnnotation":
            child_ann = cast(ClassificationAnnotation, child_ann)
            sub_job_resp = _classification_annotation_to_json_response(child_ann, other_annotations)

        elif child_ann["__typename"] == "RankingAnnotation":
            child_ann = cast(RankingAnnotation, child_ann)
            sub_job_resp = _ranking_annotation_to_json_response(child_ann)

        elif child_ann["__typename"] == "TranscriptionAnnotation":
            child_ann = cast(TranscriptionAnnotation, child_ann)
            sub_job_resp = _transcription_annotation_to_json_response(child_ann)

        else:
            raise NotImplementedError(
                f"Cannot convert child annotation to json response: {child_ann}"
            )

        for job_name, job_resp in sub_job_resp.items():
            children_json_resp[job_name] = {**children_json_resp[job_name], **job_resp}

    return children_json_resp


def _classification_annotation_to_json_response(
    annotation: ClassificationAnnotation,
    other_annotations: List[ClassicAnnotation],
) -> Dict[JobName, Dict]:
    # initialize the json response
    json_resp = {
        annotation["job"]: {
            "categories": [],
        }
    }

    # get the child annotations of the current annotation
    # and compute the json response of those child jobs
    child_annotations = _get_child_annotations(annotation, other_annotations)
    json_resp_child_jobs = (
        _compute_children_json_resp(child_annotations, other_annotations)
        if child_annotations
        else {}
    )

    # a classification job can have one or multiple categories
    categories = annotation["annotationValue"]["categories"]

    for category in categories:
        category_annotation: Dict = {"name": category}

        # search among the child annotations the ones
        # that have a path (annotationId, category)
        children_json_resp = {}
        for child_ann in child_annotations:
            if [annotation["id"], category] in child_ann["path"] and child_ann[
                "job"
            ] in json_resp_child_jobs:
                children_json_resp[child_ann["job"]] = json_resp_child_jobs[child_ann["job"]]

        if children_json_resp:
            category_annotation["children"] = children_json_resp

        json_resp[annotation["job"]]["categories"].append(category_annotation)

    return json_resp
