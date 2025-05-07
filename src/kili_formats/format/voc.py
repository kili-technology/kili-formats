from typing import Dict, Sequence
import xml.etree.ElementTree as ET
from xml.dom import minidom

from kili_formats.tool.base import reverse_rotation_vertices


def convert_from_kili_to_voc_format(response: Dict, width: int, height: int, parameters: Dict, valid_jobs: Sequence[str]) -> str:
    xml_label = ET.Element("annotation")

    _provide_voc_headers(xml_label, width, height, parameters=parameters)

    _parse_annotations(response, xml_label, width, height, valid_jobs)

    xmlstr = minidom.parseString(ET.tostring(xml_label)).toprettyxml(indent="   ")

    return xmlstr

def _provide_voc_headers(xml_label: ET.Element, width: int, height: int, parameters: Dict) -> None:
    folder = ET.SubElement(xml_label, "folder")
    folder.text = parameters.get("folder", "")

    filename = ET.SubElement(xml_label, "filename")
    filename.text = parameters.get("filename", "")

    path = ET.SubElement(xml_label, "path")
    path.text = parameters.get("path", "")

    source = ET.SubElement(xml_label, "source")
    database = ET.SubElement(source, "database")
    database.text = "Kili Technology"

    size = ET.SubElement(xml_label, "size")
    width_xml = ET.SubElement(size, "width")
    width_xml.text = str(width)
    height_xml = ET.SubElement(size, "height")
    height_xml.text = str(height)
    depth = ET.SubElement(size, "depth")
    depth.text = parameters.get("depth", "3")

    segmented = ET.SubElement(xml_label, "segmented")
    segmented.text = 0  # type: ignore

def _parse_annotations(response: Dict, xml_label: ET.Element, width: int, height:int, valid_jobs: Sequence[str]) -> None:
    # pylint: disable=too-many-locals
    rotation_val = 0
    if "ROTATION_JOB" in response:
        rotation_val = response["ROTATION_JOB"]["rotation"]
    for job_name, job_response in response.items():
        if job_name not in valid_jobs:
            continue
        if "annotations" in job_response:
            annotations = job_response["annotations"]
            for annotation in annotations:
                vertices = annotation["boundingPoly"][0]["normalizedVertices"]
                categories = annotation["categories"]
                for category in categories:
                    annotation_category = ET.SubElement(xml_label, "object")
                    name = ET.SubElement(annotation_category, "name")
                    name.text = category["name"]
                    job_name_xml = ET.SubElement(annotation_category, "job_name")
                    job_name_xml.text = job_name
                    pose = ET.SubElement(annotation_category, "pose")
                    pose.text = "Unspecified"
                    truncated = ET.SubElement(annotation_category, "truncated")
                    truncated.text = "0"
                    difficult = ET.SubElement(annotation_category, "difficult")
                    difficult.text = "0"
                    occluded = ET.SubElement(annotation_category, "occluded")
                    occluded.text = "0"
                    bndbox = ET.SubElement(annotation_category, "bndbox")
                    vertices_before_rotate = reverse_rotation_vertices(vertices, rotation_val)
                    x_vertices = [v["x"] * width for v in vertices_before_rotate]
                    y_vertices = [v["y"] * height for v in vertices_before_rotate]
                    xmin = ET.SubElement(bndbox, "xmin")
                    xmin.text = str(round(min(x_vertices)))
                    xmax = ET.SubElement(bndbox, "xmax")
                    xmax.text = str(round(max(x_vertices)))
                    ymin = ET.SubElement(bndbox, "ymin")
                    ymin.text = str(round(min(y_vertices)))
                    ymax = ET.SubElement(bndbox, "ymax")
                    ymax.text = str(round(max(y_vertices)))