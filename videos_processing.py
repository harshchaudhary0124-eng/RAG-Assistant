# This code is for preprocessing yours videos in "video" folder , cleaning it , giving it a proper name
# and then storing in "final_videos" folder which gets converted to .mp3 file in "final_audios" folder

import os
import shutil
import subprocess

def prepare_final_videos(input_folder: str = "video",
                        output_folder: str = "final_videos") -> None:
    """
    Preprocessing the raw videos for "video" folder and then cleaning and saving to "final_videos" folder .
    
    Example:
        SSYouTube.online_CSS Exercise 5 - Design this Layout#37_480p.mp4
    becomes:
        37 CSS Exercise 5 - Design this Layout.mp4
    """
    # Listing all files in the source folder
    files = os.listdir(input_folder)

    # Creating the output folder if it doesn't exist
    os.makedirs(output_folder, exist_ok=True)

    for file in files:

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
    Converting all .mp4 files in "final_videos" folder to .mp3 files in "final_audios" folder for translating and transcribing
    using ffmpeg.
    """
    # Creating the output folder if it doesn't exist
    os.makedirs(audio_folder, exist_ok=True)

    for video in os.listdir(video_folder):
        if not video.endswith(".mp4"):
            continue

        name = video.split(".")[0]

        input_path = os.path.join(video_folder, video)
        output_path = os.path.join(audio_folder, f"{name}.mp3")

        print(f"Converting {input_path} → {output_path}")

        subprocess.run(
            [
                "ffmpeg",
                "-i", input_path,
                "-vn",
                "-ab", "192k",
                output_path,
            ],
            check=False, 
        )

def main():
    print("\nPreparing videos")
    prepare_final_videos()

    print("\nExtracting audio")
    extract_audio_from_videos()

    print("Video processing completed.\n")


if __name__ == "__main__":
    main()


# if __name__ == "__main__":
#     prepare_final_videos()
#     extract_audio_from_videos()
