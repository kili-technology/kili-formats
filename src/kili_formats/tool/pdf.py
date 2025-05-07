from typing import Dict

from kili_formats.exceptions import NotCompatibleOptions
from kili_formats.media.common import scale_all_vertices


def scale_normalized_vertices_pdf_annotation(annotation: Dict, asset: Dict, **kwargs) -> None:
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
            scale_normalized_vertices_pdf_annotation(ann, asset, **kwargs)

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
                    "vertices": scale_all_vertices(
                        value["normalizedVertices"],
                        width=page_number_to_dimensions[page_number]["width"],
                        height=page_number_to_dimensions[page_number]["height"],
                    ),
                }
                for value, page_number in zip(annotation[key], annotation["pageNumberArray"])
            ]