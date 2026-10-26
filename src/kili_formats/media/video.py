"""Tools for export with videos."""

import os
import shutil
from pathlib import Path
from tempfile import TemporaryDirectory
from typing import TYPE_CHECKING, Dict, List, Optional, Tuple

from kili_formats.exceptions import NotExportableAssetError
from kili_formats.media.image import get_frame_dimensions
from kili_formats.tool.naming import frame_name, safe_path

if TYPE_CHECKING:
    import ffmpeg

ffmpeg_installed = True
try:
    import ffmpeg
except ImportError:
    ffmpeg_installed = False


class FFmpegError(Exception):
    """Errors related to ffmpeg."""


def get_video_and_frame_dimensions(
    asset: Dict,
) -> Tuple[int, int]:
    """Get a video width and height, and a frame width and height."""
    width = height = 0
    if "resolution" in asset and asset["resolution"] is not None:
        width = asset["resolution"]["width"]
        height = asset["resolution"]["height"]
        return width, height
    if isinstance(asset["jsonContent"], list) and Path(asset["jsonContent"][0]).is_file():
        width, height = get_frame_dimensions(asset)
    elif Path(asset["content"]).is_file():
        width, height = get_video_dimensions(asset)
    else:
        raise NotExportableAssetError(
            f"Could not find video dimensions for asset with externalId '{asset['externalId']}'. Please"
            " use `kili.update_properties_in_assets()` to update the resolution of your asset. Or use"
            " `kili.export_labels(with_assets=True).`"
        )
    return width, height


def get_video_dimensions(asset: Dict) -> Tuple:
    """Get a video width and height."""
    if not ffmpeg_installed:
        raise ImportError("Install with `pip install kili-formats[video]` to use this feature.")
    if "resolution" in asset and asset["resolution"] is not None:
        return (asset["resolution"]["width"], asset["resolution"]["height"])

    if Path(asset["content"]).is_file():
        probe = ffmpeg.probe(str(asset["content"]))
        video_info = next(s for s in probe["streams"] if s["codec_type"] == "video")
        width = video_info["width"]
        height = video_info["height"]
        return width, height

    raise NotExportableAssetError(
        f"Could not find video dimensions for asset with externalId '{asset['externalId']}'. Please"
        " use `kili.update_properties_in_assets()` to update the resolution of your asset. Or use"
        " `kili.export_labels(with_assets=True).`"
    )


def cut_video(
    video_path: Path, asset: Dict, leading_zeros: int, output_dir: Optional[Path]
) -> List[Path]:
    """Extract frames from video, matching import behavior for VFR videos.

    The frames are returned in order, named `<externalId>_<n>`: padded to `leading_zeros`, or to
    the width of the number of frames when it is 0, as `frame_name` names them. An external
    id holding a slash puts them in a subfolder of `output_dir`, one that stays inside it.
    """
    if not ffmpeg_installed:
        raise ImportError("Install with `pip install kili-formats[video]` to use this feature.")
    output_dir = output_dir or video_path.parent
    output_dir.mkdir(parents=True, exist_ok=True)

    should_keep_native_frame_rate = True
    final_framerate = None

    if "jsonMetadata" in asset and "processingParameters" in asset["jsonMetadata"]:
        processing_params = asset["jsonMetadata"]["processingParameters"]
        should_keep_native_frame_rate = processing_params.get("shouldKeepNativeFrameRate", True)
        final_framerate = processing_params.get("framesPlayedPerSecond")

    if final_framerate is None:
        try:
            probe = ffmpeg.probe(str(video_path))
            video_info = next(s for s in probe["streams"] if s["codec_type"] == "video")
            # avg_frame_rate is total # of frames / total duration
            # r_frame_rate is the lowest framerate with which all timestamps can be represented
            # accurately (it is the least common multiple of all framerates in the stream)
            frame_rate_string = video_info["r_frame_rate"].split("/")
            final_framerate = int(frame_rate_string[0]) / int(frame_rate_string[1])
        except ffmpeg.Error as error:
            raise FFmpegError(f"ffmpeg error for asset {video_path.name}: {error}") from error

    output_frames = []
    try:
        with TemporaryDirectory() as temp_dir:
            output_pattern = os.path.join(str(temp_dir), "%d.jpg")

            stream = ffmpeg.input(str(video_path))
            if not should_keep_native_frame_rate:
                stream = stream.filter("fps", fps=final_framerate, round="up")
            _extract_frames(stream, output_pattern, keep_timestamps=should_keep_native_frame_rate)

            # In frame order: by index, not by name, where "10" sorts before "2"
            indexes = sorted(int(Path(file).stem) for file in os.listdir(temp_dir))
            for idx in indexes:
                if leading_zeros > 0:
                    new_filename = (
                        f"{safe_path(asset['externalId'])}_{str(idx + 1).zfill(leading_zeros)}.jpg"
                    )
                else:
                    new_filename = f"{frame_name(asset['externalId'], idx, len(indexes))}.jpg"
                (output_dir / new_filename).parent.mkdir(parents=True, exist_ok=True)
                shutil.move(str(Path(temp_dir) / f"{idx}.jpg"), str(output_dir / new_filename))
                output_frames.append(output_dir / new_filename)
    except ffmpeg.Error as error:
        raise FFmpegError(f"ffmpeg error for asset {video_path.name}: {error}") from error

    return output_frames


def _extract_frames(stream, output_pattern: str, keep_timestamps: bool) -> None:
    """Write the stream's frames: each as decoded, or at a constant rate.

    ffmpeg 5.1 replaced -vsync with -fps_mode, and recent ones refuse -vsync: an older one, which
    knows -vsync alone, is asked again with it.
    """
    try:
        stream.output(
            output_pattern,
            start_number=0,
            **{"qscale:v": 1, "fps_mode": "passthrough" if keep_timestamps else "cfr", "an": None},
        ).run(capture_stdout=True, capture_stderr=True)
    except ffmpeg.Error as error:
        if b"fps_mode" not in (error.stderr or b""):
            raise
        stream.output(
            output_pattern,
            start_number=0,
            **{"qscale:v": 1, "vsync": "0" if keep_timestamps else "1", "an": None},
        ).run(capture_stdout=True, capture_stderr=True)
