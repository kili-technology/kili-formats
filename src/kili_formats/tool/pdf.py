from typing import Dict, List, Tuple

from kili_formats.exceptions import NotCompatibleOptions
from kili_formats.media.common import scale_all_vertices


def scale_normalized_vertices_pdf_annotation(annotation: Dict, asset: Dict, **kwargs) -> None:
    """Scale normalized vertices of a PDF annotation.

    PDF annotations are different from image annotations because the asset width/height can vary.

    PDF only have BBox detection, so we only scale the boundingPoly and polys keys.
    A polygon on a page whose size the asset does not hold keeps its normalizedVertices only.
    """
    is_label_rotated = kwargs.get("is_label_rotated", False)

    if is_label_rotated:
        raise NotCompatibleOptions("PDF labels cannot be rotated")

    if "annotations" in annotation:
        # pdf annotations have two layers of "annotations"
        # https://docs.kili-technology.com/reference/export-object-entity-detection-and-relation#ner-in-pdfs
        for ann in annotation["annotations"]:
            scale_normalized_vertices_pdf_annotation(ann, asset, **kwargs)

    # The k-th ring of polys[0].normalizedVertices is on page pageNumberArray[k];
    # boundingPoly pairs its rings with boundingPolyPageNumberArray the same way.
    if "polys" in annotation and "boundingPoly" in annotation:
        page_sizes = {
            page_resolution["pageNumber"]: (page_resolution["width"], page_resolution["height"])
            for page_resolution in asset.get("pageResolutions") or []
        }
        page_numbers = annotation.get("pageNumberArray") or []
        _scale_polygons(annotation["polys"], page_numbers, page_sizes)
        _scale_polygons(
            annotation["boundingPoly"],
            annotation.get("boundingPolyPageNumberArray") or page_numbers,
            page_sizes,
        )


def _scale_polygons(
    polygons: List[Dict], page_numbers: List[int], page_sizes: Dict[int, Tuple[int, int]]
) -> None:
    """Add pixel `vertices` to each polygon whose rings all lie on a page of known size.

    A polygon's normalizedVertices is a list of rings, or a single ring. Rings are paired with
    page_numbers by index, across the polygons.
    """
    ring_index = 0
    for polygon in polygons:
        normalized_vertices = polygon["normalizedVertices"]
        is_single_ring = not normalized_vertices or isinstance(normalized_vertices[0], dict)
        rings = [normalized_vertices] if is_single_ring else normalized_vertices
        sizes = [
            page_sizes[page_number]
            for page_number in page_numbers[ring_index : ring_index + len(rings)]
            if page_number in page_sizes
        ]
        ring_index += len(rings)
        if len(sizes) < len(rings):
            continue
        vertices = [
            scale_all_vertices(ring, width=width, height=height)
            for ring, (width, height) in zip(rings, sizes)
        ]
        polygon["vertices"] = vertices[0] if is_single_ring else vertices
