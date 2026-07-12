import subprocess
from pathlib import Path


def merge_audio_video(
        ffmpeg_path,
        video_file,
        audio_file,
        output_file,
):
    subprocess.run([
        ffmpeg_path,
        "-i", video_file,
        "-i", audio_file,
        "-c:v", "copy",
        "-c:a", "aac",
        "-strict", "experimental",
        output_file,
    ])


def merge_mp4_m4a(ffmpeg_path):
    mp4_files = sorted(Path("input").glob("*.mp4"))
    m4a_files = sorted(Path("input").glob("*.m4a"))

    Path("output").mkdir(exist_ok=True)

    # For each mp4 file
    for mp4_file in mp4_files:
        for m4a_file in m4a_files:
            if mp4_file.stem == m4a_file.stem:
                # If there is a matching m4a file, merge the files and break the loop
                output_file = Path("output") / f"{mp4_file.stem}.mp4"
                merge_audio_video(ffmpeg_path, mp4_file, m4a_file, output_file)
                break
