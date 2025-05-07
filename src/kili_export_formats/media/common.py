from typing import Dict, List


def scale_all_vertices(object_, width: int, height: int):
    if isinstance(object_, List):
        return [scale_all_vertices(obj, width=width, height=height) for obj in object_]

    if isinstance(object_, Dict):
        if sorted(object_.keys()) == ["x", "y"]:
            return _scale_vertex(object_, width=width, height=height)
        return {
            key: scale_all_vertices(value, width=width, height=height)
            for key, value in object_.items()
        }
    return object_


def get_asset_dimensions(asset: Dict):
    """Returns the width and height of the asset."""
    resolution = asset["resolution"]
    return resolution["width"], resolution["height"]


def _scale_vertex(vertex: Dict, width: int, height: int) -> Dict:
    return {"x": vertex["x"] * width, "y": vertex["y"] * height}
 