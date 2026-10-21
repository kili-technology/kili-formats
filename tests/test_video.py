from pathlib import Path

import pytest

from kili_formats.media import video


class _FfmpegError(Exception):
    def __init__(self, stderr: bytes):
        super().__init__(stderr)
        self.stderr = stderr


class _Ffmpeg:
    """ffmpeg-python as cut_video calls it: writes `frames` frames, `0.jpg`, `1.jpg`…, into the
    output pattern's folder; refuses `-fps_mode` when `knows_fps_mode` is False, as an ffmpeg older
    than 5.1 does."""

    Error = _FfmpegError

    def __init__(self, frames: int, knows_fps_mode: bool = True):
        self.frames = frames
        self.knows_fps_mode = knows_fps_mode
        self.outputs = []

    def input(self, _path):
        return self

    def filter(self, *_args, **_kwargs):
        return self

    def output(self, pattern, **kwargs):
        self.outputs.append(kwargs)
        self.pattern = pattern
        return self

    def run(self, **_kwargs):
        if "fps_mode" in self.outputs[-1] and not self.knows_fps_mode:
            raise _FfmpegError(b"Unrecognized option 'fps_mode'.")
        for index in range(self.frames):
            Path(self.pattern.replace("%d", str(index))).write_bytes(str(index).encode())


ASSET = {
    "externalId": "clip",
    "jsonMetadata": {
        "processingParameters": {"shouldKeepNativeFrameRate": True, "framesPlayedPerSecond": 25}
    },
}


@pytest.fixture
def fake_ffmpeg(monkeypatch):
    def install(frames, knows_fps_mode=True):
        ffmpeg = _Ffmpeg(frames, knows_fps_mode)
        monkeypatch.setattr(video, "ffmpeg", ffmpeg, raising=False)
        monkeypatch.setattr(video, "ffmpeg_installed", True)
        return ffmpeg

    return install


def test_cut_video_returns_the_frames_in_order(tmp_path, fake_ffmpeg):
    fake_ffmpeg(12)

    frames = video.cut_video(tmp_path / "clip.mp4", ASSET, 0, tmp_path / "out")

    # By index, not by name, where "10" sorts before "2"
    assert [frame.name for frame in frames] == [f"clip_{i:02d}.jpg" for i in range(1, 13)]
    assert [frame.read_bytes() for frame in frames] == [str(i).encode() for i in range(12)]


def test_cut_video_asks_an_older_ffmpeg_with_vsync(tmp_path, fake_ffmpeg):
    ffmpeg = fake_ffmpeg(2, knows_fps_mode=False)

    frames = video.cut_video(tmp_path / "clip.mp4", ASSET, 0, tmp_path / "out")

    assert [output.get("fps_mode") for output in ffmpeg.outputs] == ["passthrough", None]
    assert ffmpeg.outputs[1]["vsync"] == "0"
    assert len(frames) == 2


def test_cut_video_keeps_the_frames_inside_the_output_folder(tmp_path, fake_ffmpeg):
    fake_ffmpeg(2)
    asset = {**ASSET, "externalId": "../../dir/clip"}

    frames = video.cut_video(tmp_path / "clip.mp4", asset, 0, tmp_path / "out")

    assert frames == [tmp_path / "out" / "dir" / f"clip_{i}.jpg" for i in (1, 2)]
    assert all(frame.is_file() for frame in frames)
