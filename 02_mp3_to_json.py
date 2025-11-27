"""
mp3_to_json.py

Transcribes all .mp3 files in the `final_audios` folder using Whisper and
saves the output as JSON files in the `new_jsons` folder.

For each audio file:
- Extracts the lecture number and title from the filename.
- Runs Whisper with:
    - model: "medium"
    - language: "hi"
    - task: "translate"
- Stores segment-wise chunks with metadata:
    - number, title, start, end, text
- Stores the full transcript text as well.
"""

import json
import os

import whisper


def transcribe_audios_to_json(
    audio_folder: str = "final_audios",
    output_folder: str = "new_jsons",
    model_name: str = "medium",
) -> None:
    """
    Transcribe all .mp3 files in `audio_folder` and save JSON files
    into `output_folder` using the specified Whisper `model_name`.
    """
    # Load Whisper model once
    model = whisper.load_model(model_name)

    # Ensure output folder exists
    os.makedirs(output_folder, exist_ok=True)

    audios = os.listdir(audio_folder)
    print("Process has started")

    for audio in audios:
        # Only process .mp3 files
        if not audio.endswith(".mp3"):
            continue

        name = audio.split(".")[0]
        number = audio.split(" ")[0]  # e.g., "20"
        title = name[3:]              # remove "<number> " from the start

        print(title)

        # Run transcription
        result = model.transcribe(
            audio=os.path.join(audio_folder, audio),
            language="hi",
            task="translate",
            word_timestamps=False,
        )

        chunks = []
        for segment in result["segments"]:
            chunks.append(
                {
                    "number": number,
                    "title": title,
                    "start": segment["start"],
                    "end": segment["end"],
                    "text": segment["text"],
                }
            )

        chunks_with_metadata = {
            "chunks": chunks,
            "text": result["text"],
        }

        output_path = os.path.join(output_folder, f"{audio}.json")
        with open(output_path, "w", encoding="utf-8") as f:
            json.dump(chunks_with_metadata, f, ensure_ascii=False, indent=2)


if __name__ == "__main__":
    transcribe_audios_to_json()
