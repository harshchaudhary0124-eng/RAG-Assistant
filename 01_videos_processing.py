"""
videos_processing.py

1. Read all video files from the `video` folder.
2. Rename and copy them into the `final_videos` folder.
   - New filename format: "<number> <title>.mp4"
   - `number` and `title` are parsed from the original filename.
3. Extract audio from each MP4 file in `final_videos` using ffmpeg and
   save it as MP3 in the `final_audios` folder.
"""

import os
import shutil
import subprocess


def prepare_final_videos(input_folder: str = "video",
                         output_folder: str = "final_videos") -> None:
    """
    Copy videos from `input_folder` to `output_folder` with a cleaned name.

    The script expects filenames in the format:
        something_<title>#<number>_something.mp4

    Example:
        SSYouTube.online_CSS Exercise 5 - Design this Layout#37_480p.mp4
    becomes:
        37 CSS Exercise 5 - Design this Layout.mp4
    """
    # List all files in the source folder
    files = os.listdir(input_folder)

    # Create the output folder if it doesn't exist
    os.makedirs(output_folder, exist_ok=True)

    for file in files:
        # Extract number and title from the original filename
        # Example split:
        #   part = file.split("_")[1] -> "CSS Exercise 5 - Design this Layout#37"
        #   title = part.split("#")[0] -> "CSS Exercise 5 - Design this Layout"
        #   number = part.split("#")[1] -> "37"
        part = file.split("_")[1]
        title = part.split("#")[0]
        number = part.split("#")[1]

        formatted_video = f"{number} {title}.mp4"

        print(f"Saving: {formatted_video}")

        old_path = os.path.join(input_folder, file)
        new_path = os.path.join(output_folder, formatted_video)

        shutil.copy(old_path, new_path)
        print(f"Done with {formatted_video}")


def extract_audio_from_videos(video_folder: str = "final_videos",
                              audio_folder: str = "final_audios") -> None:
    """
    Convert all .mp4 files in `video_folder` to .mp3 files in `audio_folder`
    using ffmpeg.
    """
    # Create the output folder if it doesn't exist
    os.makedirs(audio_folder, exist_ok=True)

    for video in os.listdir(video_folder):
        if not video.endswith(".mp4"):
            continue

        name = video.split(".")[0]

        input_path = os.path.join(video_folder, video)
        output_path = os.path.join(audio_folder, f"{name}.mp3")

        print(f"Converting {input_path} → {output_path}")

        # ffmpeg command:
        # -i  : input file
        # -vn : disable video, keep only audio
        # -ab : audio bitrate
        subprocess.run(
            [
                "ffmpeg",
                "-i", input_path,
                "-vn",
                "-ab", "192k",
                output_path,
            ],
            check=False,  # set to True if you want the script to raise on error
        )


if __name__ == "__main__":
    prepare_final_videos()
    extract_audio_from_videos()
