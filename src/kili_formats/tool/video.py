from typing import Dict

from kili_formats.exceptions import NotCompatibleOptions
from kili_formats.media.common import get_asset_dimensions, scale_all_vertices
from kili_formats.tool.base import reverse_rotation_vertices


def scale_normalized_vertices_image_video_annotation(
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
                "vertices": scale_all_vertices(
                    reverse_rotation_vertices(norm_vertices_dict["normalizedVertices"], rotation),
                    width=width,
                    height=height,
                ),
            }
            for norm_vertices_dict in annotation["boundingPoly"]
        ]
    # point jobs
    if "point" in annotation:
        annotation["pointPixels"] = scale_all_vertices(
            annotation["point"], width=width, height=height
        )

    # line, vector jobs
    if "polyline" in annotation:
        annotation["polylinePixels"] = scale_all_vertices(
            annotation["polyline"], width=width, height=height
        )

    # pose estimation jobs
    if "points" in annotation:
        for point_dict in annotation["points"]:
            if "point" in point_dict:
                point_dict["pointPixels"] = scale_all_vertices(
                    point_dict["point"], width=width, height=height
                )

