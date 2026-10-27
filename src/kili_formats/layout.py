"""The layout of an export: which jobs a format takes, which labels and frames of an asset it
writes and under which names, the YOLO datasets with their class and label files, and the files
beside them.

The export service and the SDK both lay their exports out with these, so that they write the same
files; each only fetches the assets, downloads their media and writes what these return. This
module is public: both import it, so a change to its names or signatures is a versioned one.
"""

import json
import mimetypes
from datetime import datetime
from pathlib import PurePosixPath
from typing import Dict, List, Literal, NamedTuple, Optional, Sequence, Tuple

from kili_formats.format.yolo import (
    convert_from_kili_to_yolo_format,
    get_category_full_name,
)
from kili_formats.tool.naming import frame_indexes, frame_name, safe_path
from kili_formats.types import Job, JobCategory, JobTool, YoloTask

# The formats laid out here, named as the SDK names them. "yolo" is the YOLO format, the
# Ultralytics dataset the Kili app and the SDK export. "yolo_v4" to "yolo_v8" are the SDK's
# deprecated YOLO formats, kept for it until it drops them: "yolo_v8" writes the files of "yolo".
LayoutFormat = Literal["coco", "pascal_voc", "yolo", "yolo_v4", "yolo_v5", "yolo_v7", "yolo_v8"]

# How a YOLO export (and the deprecated YOLO v5, v7 and v8) writes the bounding boxes: "box", the
# upright box around each, for the detect task; "obb", their four corners, for the obb task;
# "polygon", their four corners, in the segment task
YoloBoundingBoxes = Literal["box", "obb", "polygon"]

BOX_TOOLS = (JobTool.RECTANGLE,)
SEGMENT_TOOLS = (JobTool.POLYGON, JobTool.SEMANTIC)
SHAPE_TOOLS = BOX_TOOLS + SEGMENT_TOOLS

# The tools whose jobs each format exports: Pascal VOC and YOLO v4 hold rectangles only
_FORMAT_TOOLS: Dict[str, Tuple[JobTool, ...]] = {
    "coco": SHAPE_TOOLS,
    "pascal_voc": BOX_TOOLS,
    "yolo": SHAPE_TOOLS,
    "yolo_v4": BOX_TOOLS,
    "yolo_v5": SHAPE_TOOLS,
    "yolo_v7": SHAPE_TOOLS,
    "yolo_v8": SHAPE_TOOLS,
}

_BOX_TASKS: Dict[str, YoloTask] = {"box": "detect", "obb": "obb", "polygon": "segment"}

README_FILE = "README.kili.txt"
REMOTE_ASSETS_FILE = "remote_assets.csv"
REMOTE_ASSETS_HEADER = ("external id", "url", "label file")
VIDEO_METADATA_FILE = "video_meta.json"

# The image extensions, as YOLO reads them, and the extension each image content type is saved with
IMAGE_EXTENSIONS = (
    ".avif",
    ".bmp",
    ".dng",
    ".gif",
    ".heic",
    ".heif",
    ".ico",
    ".jp2",
    ".jpeg",
    ".jpg",
    ".mpo",
    ".png",
    ".tif",
    ".tiff",
    ".webp",
)
_IMAGE_TYPE_EXTENSIONS = {
    "image/avif": ".avif",
    "image/bmp": ".bmp",
    "image/gif": ".gif",
    "image/heic": ".heic",
    "image/heif": ".heif",
    "image/jp2": ".jp2",
    "image/jpeg": ".jpg",
    "image/jpg": ".jpg",
    "image/pjpeg": ".jpg",
    "image/png": ".png",
    "image/tiff": ".tif",
    "image/vnd.microsoft.icon": ".ico",
    "image/webp": ".webp",
    "image/x-icon": ".ico",
}


def jobs_with_tools(json_interface: Optional[Dict], tools: Sequence[str]) -> Dict[str, Job]:
    """The object detection jobs of the interface with one of `tools`, model jobs left out."""
    return {
        job_id: job
        for job_id, job in ((json_interface or {}).get("jobs") or {}).items()
        if job.get("mlTask") == "OBJECT_DETECTION"
        and any(tool in (job.get("tools") or []) for tool in tools)
        and not job.get("isModel")
    }


def exported_jobs(json_interface: Optional[Dict], label_format: LayoutFormat) -> Dict[str, Job]:
    """The jobs a format exports: the shapes' jobs; the bounding box jobs alone for Pascal VOC and
    YOLO v4."""
    return jobs_with_tools(json_interface, _FORMAT_TOOLS[label_format])


def labels_of(asset: Dict) -> List[Dict]:
    """The labels of an asset an export writes, whichever its query fetched: the latest, the latest
    per step or per labeler, or all of them."""
    labels = [asset["latestLabel"]] if asset.get("latestLabel") else []
    for field in ("latestLabels", "labels"):
        labels += [label for label in asset.get(field) or [] if label is not None]
    return labels


def label_suffix(index: int, count: int) -> str:
    """What the files of an asset's `index`-th label (from 1) of `count` are suffixed with: none
    for a single label."""
    return f"_label{index}" if count > 1 else ""


def one_asset_per_label(asset: Dict) -> List[Dict]:
    """The asset once per label, each copy holding its label as its latest one, its media and
    external id shared: an image is never written twice."""
    labels = labels_of(asset)
    return [
        {
            **{key: value for key, value in asset.items() if key not in ("latestLabels", "labels")},
            "latestLabel": label,
        }
        for label in labels
    ]


def image_filename(name: str, content_type: Optional[str] = None) -> str:
    """The file name of a downloaded media: `name`, with the extension of its content type unless
    it already has one. An image always ends with an image extension: YOLO reads no other. The name
    stays inside the folder it is written to, whatever its external id."""
    name = safe_path(name)
    suffix = PurePosixPath(name).suffix.lower()
    if suffix in IMAGE_EXTENSIONS:
        return name
    mimetype = (content_type or "").split(";")[0].strip().lower()
    extension = _IMAGE_TYPE_EXTENSIONS.get(mimetype)
    if extension is None and mimetype and mimetype != "application/octet-stream":
        extension = mimetypes.guess_extension(mimetype)
    if suffix and suffix in [extension, *mimetypes.guess_all_extensions(mimetype)]:
        return name
    if mimetype.startswith("image/") or not (suffix and mimetypes.types_map.get(suffix)):
        return f"{name}{extension or ''}"
    return name


def label_frame_count(label: Dict) -> int:
    """The number of frames a video label covers, up to its last one."""
    indexes = frame_indexes(label.get("jsonResponse") or {})
    return indexes[-1] + 1 if indexes else 0


def with_annotation_types(json_response: Dict, json_interface: Optional[Dict]) -> Dict:
    """The json response, its annotations without a type typed after their job's shape tool when
    the job has a single one: labels imported without types are exported as the job draws them."""
    jobs = (json_interface or {}).get("jobs") or {}
    typed = dict(json_response)
    for job_id, job_response in json_response.items():
        tools = [
            tool for tool in (jobs.get(job_id) or {}).get("tools") or [] if tool in SHAPE_TOOLS
        ]
        annotations = (
            (job_response or {}).get("annotations") if isinstance(job_response, dict) else None
        )
        if len(tools) != 1 or not annotations:
            continue
        typed[job_id] = {
            **job_response,
            "annotations": [
                annotation if annotation.get("type") else {**annotation, "type": tools[0]}
                for annotation in annotations
            ],
        }
    return typed


class LabelFile(NamedTuple):
    """A file an export writes for a label of an asset, or for a frame of a video's label.

    `stem` names it, extension aside, the label's suffix included; `image` names the image it
    describes, extension aside, shared by every label of the asset; `frame` is the video frame's
    index; `json_response` is the label's or the frame's, its annotations typed.
    """

    stem: str
    image: str
    frame: Optional[int]
    json_response: Dict


def asset_label_files(
    asset: Dict,
    input_type: str,
    job_ids: Sequence[str],
    frame_count: int = 0,
    json_interface: Optional[Dict] = None,
) -> List[LabelFile]:
    """The files an export writes for an asset: one per label of an image; for a video, one per
    label and frame holding a shape of `job_ids`, frames with none left out.

    Several labels are told apart by their suffix, `<name>_label<n>`, their images shared. A
    video's frames are named after `frame_count`, the video's number of frames, or the frames its
    labels cover when it is not known.
    """
    labels = labels_of(asset)
    external_id = safe_path(asset["externalId"])
    files = []
    if input_type != "VIDEO":
        for index, label in enumerate(labels, start=1):
            files.append(
                LabelFile(
                    f"{external_id}{label_suffix(index, len(labels))}",
                    external_id,
                    None,
                    with_annotation_types(label.get("jsonResponse") or {}, json_interface),
                )
            )
        return files

    count = frame_count or max((label_frame_count(label) for label in labels), default=0)
    for index, label in enumerate(labels, start=1):
        json_response = label.get("jsonResponse") or {}
        for frame in frame_indexes(json_response):
            response = json_response.get(str(frame), json_response.get(frame)) or {}  # type: ignore
            if not any((response.get(job_id) or {}).get("annotations") for job_id in job_ids):
                continue
            name = frame_name(external_id, frame, count)
            files.append(
                LabelFile(
                    f"{name}{label_suffix(index, len(labels))}",
                    name,
                    frame,
                    with_annotation_types(response, json_interface),
                )
            )
    return files


def video_metadata(frames_by_asset: Dict[str, List[str]]) -> str:
    """The content of the video metadata file: each video asset's frame names, by external id."""
    return json.dumps(frames_by_asset, sort_keys=True, indent=4)


def readme(
    project: Dict,
    label_format: str,
    export_type: str,
    date: Optional[datetime] = None,
    notes: Sequence[str] = (),
) -> str:
    """The content of the README file of an export, `notes` after its description."""
    return (
        "Exported Labels from KILI\n=========================\n\n"
        f"- Project name: {project['title']}\n"
        f"- Project identifier: {project['id']}\n"
        f"- Project description: {project.get('description') or ''}\n"
        f"- Export date: {(date or datetime.now()).strftime(r'%Y%m%d-%H%M%S')}\n"
        f"- Exported format: {label_format}\n"
        f"- Exported labels: {export_type}\n" + "".join(f"\n{note}\n" for note in notes)
    )


class YoloFolder(NamedTuple):
    """A folder of a YOLO export: its task, its classes, whether it writes the bounding boxes as
    polygons, whether its classes are named after their job too, and where the images are from it.
    """

    task: YoloTask
    categories: Dict[str, JobCategory]
    boxes_as_polygons: bool = False
    with_job: bool = True
    images: str = "images"


def _box_task(label_format: LayoutFormat, bounding_boxes: YoloBoundingBoxes) -> YoloTask:
    """The task the bounding boxes are written for. YOLO v4 has no other task than detect."""
    return "detect" if label_format == "yolo_v4" else _BOX_TASKS[bounding_boxes]


def yolo_tasks(
    json_interface: Optional[Dict],
    label_format: LayoutFormat,
    bounding_boxes: YoloBoundingBoxes = "box",
) -> List[YoloTask]:
    """The tasks a YOLO export writes a dataset for: the bounding boxes' task with a bounding box
    job, then segment with a polygon or semantic job. YOLO v4 has detect only."""
    tasks: List[YoloTask] = []
    if jobs_with_tools(json_interface, BOX_TOOLS):
        tasks.append(_box_task(label_format, bounding_boxes))
    if (
        label_format != "yolo_v4"
        and jobs_with_tools(json_interface, SEGMENT_TOOLS)
        and "segment" not in tasks
    ):
        tasks.append("segment")
    return tasks


def _job_categories(job_id: str, job: Job, first_id: int = 0) -> Dict[str, JobCategory]:
    return {
        get_category_full_name(job_id, category): JobCategory(
            category_name=category, id=first_id + index, job_id=job_id
        )
        for index, category in enumerate((job.get("content") or {}).get("categories") or {})
    }


def yolo_folders(
    json_interface: Optional[Dict],
    label_format: LayoutFormat,
    split: bool,
    bounding_boxes: YoloBoundingBoxes = "box",
) -> Dict[str, YoloFolder]:
    """The folders a YOLO export writes, by path in the archive.

    Split, a folder per job, written for the job's own task: segment with a polygon or semantic
    tool, its bounding boxes as polygons; the bounding boxes' task otherwise. Merged, a folder per
    task, at the archive's root when there is one: its jobs' classes numbered one after the other.
    """
    jobs = exported_jobs(json_interface, label_format)
    if split:
        folders = {}
        for job_id, job in jobs.items():
            is_segment = label_format != "yolo_v4" and bool(
                jobs_with_tools({"jobs": {job_id: job}}, SEGMENT_TOOLS)
            )
            task = "segment" if is_segment else _box_task(label_format, bounding_boxes)
            # A job's folder is the only place for its bounding boxes
            folders[job_id] = YoloFolder(
                task,
                _job_categories(job_id, job),
                boxes_as_polygons=task == "segment",
                with_job=False,
                images="../images",
            )
        return folders

    tasks = yolo_tasks(json_interface, label_format, bounding_boxes)
    folders = {}
    for task in tasks:
        boxes_as_polygons = task == "segment" and bounding_boxes == "polygon"
        if task != "segment":
            tools = BOX_TOOLS
        else:
            tools = SHAPE_TOOLS if boxes_as_polygons else SEGMENT_TOOLS
        categories: Dict[str, JobCategory] = {}
        for job_id, job in jobs_with_tools({"jobs": jobs}, tools).items():
            categories.update(_job_categories(job_id, job, first_id=len(categories)))
        path = task if len(tasks) > 1 else ""
        folders[path] = YoloFolder(
            task, categories, boxes_as_polygons, images="../images" if path else "images"
        )
    return folders


def yolo_readme_notes(folders: Dict[str, YoloFolder]) -> List[str]:
    """What the README says of a YOLO export whose datasets have folders of their own."""
    if all(not path for path in folders):
        return []
    return [
        "Each dataset's folder holds its data.yaml and labels/; the images are shared, in images/ "
        "at the archive's root. YOLO reads a dataset's labels next to its images: to train on one, "
        "put its labels/ beside images/ (or images/ inside its folder)."
    ]


def yolo_class_file(folder: YoloFolder, label_format: LayoutFormat) -> Tuple[str, str]:
    """The name and content of a YOLO folder's class file: classes.txt for YOLO v4; data.yaml
    otherwise, its images for training and validation, its classes named after their job too when
    the folder merges several, each a quoted string, so that a name like NO stays one."""
    names = [
        f"{category.job_id}/{category.category_name}" if folder.with_job else category.category_name
        for category in folder.categories.values()
    ]
    if label_format == "yolo_v4":
        return "classes.txt", "".join(
            f"{category.id} {name}\n" for category, name in zip(folder.categories.values(), names)
        )
    images = f"train: {folder.images}\nval: {folder.images}\n"
    if label_format == "yolo_v5":
        return "data.yaml", images + "names:\n" + "".join(
            f"  {index}: {json.dumps(name)}\n" for index, name in enumerate(names)
        )
    if label_format in ("yolo", "yolo_v7", "yolo_v8"):
        quoted = ", ".join(json.dumps(name) for name in names)
        return "data.yaml", f"{images}nc: {len(names)}\nnames: [{quoted}]\n"
    raise ValueError(f"Unknown YOLO format: {label_format}")


def yolo_label_filename(name: str) -> str:
    """The YOLO label file of an image or a frame: its name, image extension aside, in .txt, as
    YOLO looks for it."""
    path = PurePosixPath(name)
    return f"{path.with_suffix('') if path.suffix.lower() in IMAGE_EXTENSIONS else name}.txt"


def yolo_label_file(json_response: Dict, folder: YoloFolder) -> str:
    """The content of a YOLO label file, for a label's json response or a frame's: a line per
    shape of the folder's jobs, written for its task.

    An export writes it even empty: the image is then a background one for the folder's task.
    """
    job_ids = list(dict.fromkeys(category.job_id for category in folder.categories.values()))
    label = {"jsonResponse": json_response}
    return "".join(
        " ".join(str(value) for value in line) + "\n"
        for job_id in job_ids
        for line in convert_from_kili_to_yolo_format(
            job_id, label, folder.categories, folder.task, folder.boxes_as_polygons
        )
    )
