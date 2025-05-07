import json
import time
from datetime import datetime
from pathlib import Path
from typing import Any, Dict, List, Optional, Tuple

from kili_formats.media.image import get_frame_dimensions, get_image_dimensions
from kili_formats.media.video import cut_video, get_video_dimensions
from kili_formats.tool.base import reverse_rotation_vertices
from kili_formats.types import Job
import numpy as np
from shapely.geometry import Polygon
from shapely.ops import polygonize
from shapely.validation import make_valid


from .types import (
    CocoAnnotation,
    CocoAnnotationModifier,
    CocoCategory,
    CocoFormat,
    CocoImage,
)

DATA_SUBDIR = "data"


# pylint: disable=too-many-arguments
def convert_from_kili_to_coco_format(
    jobs: Dict[str, Job],
    assets: List[Dict],
    output_dir: Path,
    title: str,
    project_input_type: str,
    annotation_modifier: Optional[CocoAnnotationModifier],
    merged: bool,
) -> Tuple[CocoFormat, List[Path]]:
    """Creates the following structure on the disk.

    <dataset_dir>/
        data/
            <filename0>.<ext>
            <filename1>.<ext>
            ...
        labels.json.

    We iterate on the assets and create a coco format for each asset.

    Note: the jobs should only contains elligible jobs.
    """
    infos_coco = {
        "year": time.strftime("%Y"),
        "version": "1.0",
        "description": f"{title} - Exported from Kili Python Client",
        "contributor": "Kili Technology",
        "url": "https://kili-technology.com",
        "date_created": datetime.now().isoformat(),
    }
    labels_json = CocoFormat(
        info=infos_coco,
        licenses=[],
        categories=[],
        images=[],
        annotations=[],
    )

    # Mapping category - category id
    cat_kili_id_to_coco_id, labels_json["categories"] = _get_coco_categories_with_mapping(
        jobs, merged
    )

    if merged:
        labels_json["images"], labels_json["annotations"] = _get_coco_images_and_annotations(
            jobs,
            assets,
            cat_kili_id_to_coco_id,
            project_input_type,
            annotation_modifier,
            is_single_job=False,
        )

        label_file_name = output_dir / "labels.json"
        label_file_name.parent.mkdir(parents=True, exist_ok=True)
        with label_file_name.open("w") as outfile:
            json.dump(labels_json, outfile)
        label_filenames = [label_file_name]
    else:  # split case
        label_filenames = []
        for job_name, job in jobs.items():
            labels_json["images"], labels_json["annotations"] = _get_coco_images_and_annotations(
                {job_name: job},
                assets,
                cat_kili_id_to_coco_id,
                project_input_type,
                annotation_modifier,
                is_single_job=True,
            )
            label_file_name = output_dir / job_name / "labels.json"

            label_file_name.parent.mkdir(parents=True, exist_ok=True)
            with label_file_name.open("w") as outfile:
                json.dump(labels_json, outfile)
            label_filenames.append(label_file_name)

    return labels_json, label_filenames


def _get_coco_categories_with_mapping(
    jobs: Dict[str, Job], merged: bool
) -> Tuple[Dict[str, Dict[str, int]], List[CocoCategory]]:
    """_get_coco_categories_with_mapping.

    Get the mapping between a category name in Kili of a given job and the COCO category id, and
    also return the list of COCO categories.
    """
    if merged:
        mapping_cat_name_cat_kili_id: Dict[str, str] = {}
        cat_kili_id_to_coco_id: Dict[str, Dict[str, int]] = {}
        id_offset = 0
        for job_name, job in sorted(jobs.items(), key=lambda x: x[0]):
            content = dict(job["content"])
            job_cats: Dict[str, Any] = content["categories"]
            mapping_cat_name_cat_kili_id = {
                "/".join([job_name, cat["name"]]): cat_id for cat_id, cat in job_cats.items()
            }

            cat_kili_ids = sorted(mapping_cat_name_cat_kili_id.values())
            cat_kili_id_to_coco_id[job_name] = {
                str(category_id): i + id_offset for i, category_id in enumerate(cat_kili_ids)
            }
            id_offset += len(cat_kili_ids)

    else:
        assert (
            len(list(jobs.values())) == 1
        ), "When this method is called with merged = False, the jobs should only contain 1 job"
        job_name = next(iter(jobs.keys()))
        cats = next(iter(jobs.values()))["content"]["categories"]
        mapping_cat_name_cat_kili_id = {cat["name"]: cat_id for cat_id, cat in cats.items()}
        cat_kili_ids = list(mapping_cat_name_cat_kili_id.values())
        cat_kili_id_to_coco_id = {
            job_name: {str(category_id): i for i, category_id in enumerate(cat_kili_ids)}
        }

    return cat_kili_id_to_coco_id, _get_coco_categories(cat_kili_id_to_coco_id, merged)


# pylint: disable=too-many-locals
def _get_coco_images_and_annotations(
    jobs: Dict[str, Job],
    assets: List[Dict],
    cat_kili_id_to_coco_id: Dict[str, Dict[str, int]],
    project_input_type: str,
    annotation_modifier: Optional[CocoAnnotationModifier],
    is_single_job: bool,
) -> Tuple[List[CocoImage], List[CocoAnnotation]]:
    if project_input_type == "IMAGE":
        return _get_images_and_annotation_for_images(
            jobs, assets, cat_kili_id_to_coco_id, annotation_modifier, is_single_job
        )

    if project_input_type == "VIDEO":
        return _get_images_and_annotation_for_videos(
            jobs, assets, cat_kili_id_to_coco_id, annotation_modifier, is_single_job
        )

    raise NotImplementedError(f"No conversion to COCO possible for input type {project_input_type}")

def _get_images_and_annotation_for_images(
    jobs: Dict[str, Job],
    assets: List[Dict],
    cat_kili_id_to_coco_id: Dict[str, Dict[str, int]],
    annotation_modifier: Optional[CocoAnnotationModifier],
    is_single_job: bool,
) -> Tuple[List[CocoImage], List[CocoAnnotation]]:
    coco_images = []
    coco_annotations = []
    annotation_offset = 0

    for asset_i, asset in enumerate(assets):
        width, height = get_image_dimensions(asset)
        if Path(asset["content"]).is_file():
            filename = str(DATA_SUBDIR + "/" + Path(asset["content"]).name)
        else:
            filename = str(DATA_SUBDIR + "/" + asset["externalId"])
        coco_image = CocoImage(
            id=asset_i,
            license=0,
            file_name=filename,
            height=height,
            width=width,
            date_captured=None,
        )
        rotation_val = 0
        if "ROTATION_JOB" in asset["latestLabel"]["jsonResponse"]:
            rotation_val = asset["latestLabel"]["jsonResponse"]["ROTATION_JOB"]["rotation"]
        coco_images.append(coco_image)
        if is_single_job:
            assert len(list(jobs.keys())) == 1
            job_name = next(iter(jobs.keys()))

            if job_name not in asset["latestLabel"]["jsonResponse"]:
                coco_img_annotations = []
                # annotation offset is unchanged
            else:
                coco_img_annotations, annotation_offset = _get_coco_image_annotations(
                    asset["latestLabel"]["jsonResponse"][job_name]["annotations"],
                    cat_kili_id_to_coco_id[job_name],
                    annotation_offset,
                    coco_image,
                    annotation_modifier=annotation_modifier,
                    rotation=rotation_val,
                )
            coco_annotations.extend(coco_img_annotations)
        else:
            for job_name in jobs:
                if job_name not in asset["latestLabel"]["jsonResponse"]:
                    continue
                    # annotation offset is unchanged

                coco_img_annotations, annotation_offset = _get_coco_image_annotations(
                    asset["latestLabel"]["jsonResponse"][job_name]["annotations"],
                    cat_kili_id_to_coco_id[job_name],
                    annotation_offset,
                    coco_image,
                    annotation_modifier=annotation_modifier,
                    rotation=rotation_val,
                )
                coco_annotations.extend(coco_img_annotations)
    return coco_images, coco_annotations


def _get_images_and_annotation_for_videos(
    jobs: Dict[str, Job],
    assets: List[Dict],
    cat_kili_id_to_coco_id: Dict[str, Dict[str, int]],
    annotation_modifier: Optional[CocoAnnotationModifier],
    is_single_job: bool,
) -> Tuple[List[CocoImage], List[CocoAnnotation]]:
    coco_images = []
    coco_annotations = []
    annotation_offset = 0

    for asset in assets:
        nbr_frames = len(asset.get("latestLabel", {}).get("jsonResponse", {}))
        leading_zeros = len(str(nbr_frames))

        width = height = 0
        frame_ext = ""
        # jsonContent with frames
        if isinstance(asset["jsonContent"], list) and Path(asset["jsonContent"][0]).is_file():
            width, height = get_frame_dimensions(asset)
            frame_ext = Path(asset["jsonContent"][0]).suffix

        # video with shouldUseNativeVideo set to True (no frames available)
        elif Path(asset["content"]).is_file():
            width, height = get_video_dimensions(asset)
            cut_video(asset["content"], asset, leading_zeros, Path(asset["content"]).parent)
            frame_ext = ".jpg"

        else:
            raise FileNotFoundError(f"Could not find frames or video for asset {asset}")

        for frame_i, (frame_id, json_response) in enumerate(
            asset["latestLabel"]["jsonResponse"].items()
        ):
            frame_name = f'{asset["externalId"]}_{str(int(frame_id)+1).zfill(leading_zeros)}'
            coco_image = CocoImage(
                id=frame_i + len(assets),  # add offset to avoid duplicate ids
                license=0,
                file_name=str(DATA_SUBDIR + "/" + f"{frame_name}{frame_ext}"),
                height=height,
                width=width,
                date_captured=None,
            )
            coco_images.append(coco_image)
            if is_single_job:
                job_name = next(iter(jobs.keys()))
                if job_name not in json_response:
                    coco_img_annotations = []
                    # annotation offset is unchanged
                else:
                    coco_img_annotations, annotation_offset = _get_coco_image_annotations(
                        json_response[job_name]["annotations"],
                        cat_kili_id_to_coco_id[job_name],
                        annotation_offset,
                        coco_image,
                        annotation_modifier,
                    )
                coco_annotations.extend(coco_img_annotations)
            else:
                for job_name in jobs:
                    if job_name not in asset["latestLabel"]["jsonResponse"]:
                        continue
                    coco_img_annotations, annotation_offset = _get_coco_image_annotations(
                        json_response[job_name]["annotations"],
                        cat_kili_id_to_coco_id[job_name],
                        annotation_offset,
                        coco_image,
                        annotation_modifier,
                    )

                    coco_annotations.extend(coco_img_annotations)

    return coco_images, coco_annotations


def _get_coco_image_annotations(
    annotations_: List[Dict],
    cat_kili_id_to_coco_id: Dict[str, int],
    annotation_offset: int,
    coco_image: CocoImage,
    annotation_modifier: Optional[CocoAnnotationModifier],
    rotation: int = 0,
) -> Tuple[List[CocoAnnotation], int]:
    coco_annotations = []

    annotation_j = annotation_offset

    for annotation in annotations_:  # we do not use enumerate as some annotations may be empty
        annotation_j += 1

        if not annotation:
            print("continue")
            continue
        bounding_poly = annotation["boundingPoly"]
        area, bbox, polygons = _get_coco_geometry_from_kili_bpoly(
            bounding_poly, coco_image["width"], coco_image["height"], rotation
        )
        if len(polygons[0]) < 6:  # twice the number of vertices
            print("A polygon must contain more than 2 points. Skipping this polygon...")
            continue
        if bbox[2] == 0 and bbox[3] == 0:
            print("An annotation with zero dimensions has been ignored.")
            continue

        categories = annotation["categories"]
        coco_annotation = CocoAnnotation(
            id=annotation_j,
            image_id=coco_image["id"],
            category_id=cat_kili_id_to_coco_id[categories[0]["name"]],
            bbox=bbox,
            # Objects have only one connected part.
            # But a type of object can appear several times on the same image.
            # The limitation of the single connected part comes from Kili.
            segmentation=polygons,
            area=area,
            iscrowd=0,
        )

        if annotation_modifier:
            coco_annotation = annotation_modifier(
                dict(coco_annotation), dict(coco_image), annotation
            )

        coco_annotations.append(coco_annotation)
    return coco_annotations, annotation_j




def _get_coco_geometry_from_kili_bpoly(
    bounding_poly: List[Dict], asset_width: int, asset_height: int, rotation_angle: int
):
    normalized_vertices = bounding_poly[0]["normalizedVertices"]
    vertices_before_rotate = reverse_rotation_vertices(normalized_vertices, rotation_angle)
    p_x = [float(vertice["x"]) * asset_width for vertice in vertices_before_rotate]
    p_y = [float(vertice["y"]) * asset_height for vertice in vertices_before_rotate]
    poly_vertices = [(float(x), float(y)) for x, y in zip(p_x, p_y)]
    x_min, y_min = round(min(p_x)), round(min(p_y))
    x_max, y_max = round(max(p_x)), round(max(p_y))
    bbox_width, bbox_height = x_max - x_min, y_max - y_min
    area = round(_get_shoelace_area(p_x, p_y))
    polygons = [[p for vertice in poly_vertices for p in vertice]]

    # Compute and remove negative area
    if len(bounding_poly) > 1:
        for negative_bounding_poly in bounding_poly[1:]:
            negative_normalized_vertices = negative_bounding_poly["normalizedVertices"]
            negative_vertices_before_rotate = reverse_rotation_vertices(
                negative_normalized_vertices, rotation_angle
            )
            np_x = [
                float(negative_vertice["x"]) * asset_width
                for negative_vertice in negative_vertices_before_rotate
            ]
            np_y = [
                float(negative_vertice["y"]) * asset_height
                for negative_vertice in negative_vertices_before_rotate
            ]
            area -= _get_shoelace_area(np_x, np_y)
            poly_negative_vertices = [(float(x), float(y)) for x, y in zip(np_x, np_y)]
            polygons.append([p for vertice in poly_negative_vertices for p in vertice])
    bbox = [int(x_min), int(y_min), int(bbox_width), int(bbox_height)]
    return area, bbox, polygons


def _get_coco_categories(cat_kili_id_to_coco_id, merged) -> List[CocoCategory]:
    categories_coco: List[CocoCategory] = []
    for job_name, mapping in sorted(cat_kili_id_to_coco_id.items(), key=lambda x: x[0]):
        for cat_kili_id, cat_coco_id in sorted(mapping.items(), key=lambda x: x[1]):
            categories_coco.append(
                {
                    "id": cat_coco_id,
                    "name": cat_kili_id if not merged else f"{job_name}/{cat_kili_id}",
                    "supercategory": job_name,
                }
            )

    return categories_coco


# Shoelace formula, implementation from https://stackoverflow.com/a/30408825.
def _get_shoelace_area(x: List[float], y: List[float]):
    # Split self intersecting polygon into multiple polygons to compute area safely.
    polygon = Polygon(np.c_[x, y])
    polygons = polygonize(make_valid(polygon))

    area = 0

    for poly in polygons:
        p_xx, p_yy = poly.exterior.coords.xy
        p_x = p_xx.tolist()
        p_y = p_yy.tolist()
        area += 0.5 * np.abs(np.dot(p_x, np.roll(p_y, 1)) - np.dot(p_y, np.roll(p_x, 1)))

    return area
