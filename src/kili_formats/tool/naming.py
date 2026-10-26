"""How an export names the files of an asset: its path from its external id, its video frames."""

from typing import Dict, List


def safe_path(name: str) -> str:
    """`name` as a relative path that stays inside the folder it is joined to: no `..`, `.` or
    empty part, no leading `/`, a backslash read as a separator. An external id is chosen by
    whoever adds the asset, and an export writes files named after it."""
    parts = [
        part for part in str(name).replace("\\", "/").split("/") if part not in ("", ".", "..")
    ]
    return "/".join(parts) or "_"


def frame_name(external_id: str, index: int, frame_count: int) -> str:
    """The name of a video's frame, from 0, among `frame_count`: `<external id>_<n>`, numbered from
    1 and padded to the width of `frame_count`."""
    return f"{safe_path(external_id)}_{str(index + 1).zfill(len(str(frame_count)))}"


def frame_indexes(json_response: Dict) -> List[int]:
    """The frames a video label holds, by index: its keys that are numbers, `assetLevel` aside."""
    return sorted(int(key) for key in json_response if str(key).isdigit())
