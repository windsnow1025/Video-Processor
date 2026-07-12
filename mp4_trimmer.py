import json
import subprocess
from pathlib import Path


def get_video_duration(ffprobe_path, video_file):
    result = subprocess.run([
        ffprobe_path,
        "-v", "quiet",
        "-print_format", "json",
        "-show_format",
        video_file,
    ], capture_output=True, text=True)

    if result.returncode == 0:
        data = json.loads(result.stdout)
        duration = float(data["format"]["duration"])
        return duration
    else:
        raise Exception(f"Failed to get video duration: {result.stderr}")


def trim_video_end(
        ffmpeg_path,
        ffprobe_path,
        video_file,
        output_file,
        seconds_to_remove,
):
    original_duration = get_video_duration(ffprobe_path, video_file)
    new_duration = original_duration - seconds_to_remove

    if new_duration <= 0:
        raise Exception(f"Cannot remove {seconds_to_remove} seconds from a {original_duration:.2f} second video")

    subprocess.run([
        ffmpeg_path,
        "-i", video_file,
        "-t", str(new_duration),
        "-c", "copy",
        output_file,
    ])


def trim_mp4_end(ffmpeg_path, ffprobe_path, seconds_to_remove):
    mp4_files = sorted(Path("input").glob("*.mp4"))

    if len(mp4_files) != 1:
        raise Exception(f"Expected exactly one mp4 file in input directory, found {len(mp4_files)}")

    Path("output").mkdir(exist_ok=True)

    mp4_file = mp4_files[0]
    output_file = Path("output") / f"{mp4_file.stem}_trimmed.mp4"

    trim_video_end(ffmpeg_path, ffprobe_path, mp4_file, output_file, seconds_to_remove)
