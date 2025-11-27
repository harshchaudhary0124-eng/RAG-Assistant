"""
merge_chunks.py

Reads JSON transcript files from the `new_jsons` folder and merges
every `n` small chunks into a larger chunk.

For each input file:
- Group `chunks` into batches of size `n`.
- For each group, create a new chunk with:
    - number  : taken from the first original chunk
    - title   : taken from the first original chunk
    - start   : start time of the first chunk in the group
    - end     : end time of the last chunk in the group
    - text    : concatenation of all texts in the group
- Save the merged result into `final_jsons/<same_filename>.json`.
"""

import json
import math
import os


def merge_chunks_in_folder(
    input_folder: str = "new_jsons",
    output_folder: str = "final_jsons",
    group_size: int = 5,
) -> None:
    """
    Merge chunks from all JSON files in `input_folder` into bigger chunks
    of size `group_size`, and write the result into `output_folder`.
    """
    os.makedirs(output_folder, exist_ok=True)

    for filename in os.listdir(input_folder):
        if not filename.endswith(".json"):
            continue

        file_path = os.path.join(input_folder, filename)

        with open(file_path, "r", encoding="utf-8") as f:
            data = json.load(f)

        chunks = data["chunks"]
        num_chunks = len(chunks)
        num_groups = math.ceil(num_chunks / group_size)

        new_chunks = []

        for i in range(num_groups):
            start_idx = i * group_size
            end_idx = min((i + 1) * group_size, num_chunks)

            chunk_group = chunks[start_idx:end_idx]

            new_chunks.append(
                {
                    "number": chunks[0]["number"],
                    "title": chunks[0]["title"],
                    "start": chunk_group[0]["start"],
                    "end": chunk_group[-1]["end"],
                    "text": " ".join(c["text"] for c in chunk_group),
                }
            )

        output_path = os.path.join(output_folder, filename)
        with open(output_path, "w", encoding="utf-8") as json_file:
            json.dump({"chunks": new_chunks, "text": data["text"]},
                      json_file,
                      ensure_ascii=False,
                      indent=2)


if __name__ == "__main__":
    merge_chunks_in_folder()
