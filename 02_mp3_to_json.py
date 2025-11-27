import json
import os

import whisper


def transcribe_audios_to_json(
    audio_folder: str = "final_audios",
    output_folder: str = "new_jsons",
    model_name: str = "medium",
) -> None:
    """
    Transcribing all .mp3 files in "final_audios" folder and save JSON files into "new_jsons" folder using the specified Whisper `medium`.
    """
    # Loading the Whisper model once
    model = whisper.load_model(model_name)

    os.makedirs(output_folder, exist_ok=True)

    audios = os.listdir(audio_folder)
    print("Process has started")

    for audio in audios:
        
        if not audio.endswith(".mp3"):
            continue

        name = audio.split(".")[0]
        number = audio.split(" ")[0] 
        title = name[3:]              

        print(title)

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
