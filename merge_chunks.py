import json
import math
import os


def merge_chunks_in_folder(
    input_folder: str = "new_jsons",
    output_folder: str = "final_jsons",
    group_size: int = 5,
) -> None:
    """
    Merging all small chunks from all JSON files in "new_jsons" folder into bigger chunks, and write the result into "final_jsons".
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

def main():
    merge_chunks_in_folder()

if __name__ == "__main__":
    main()
    
    
# if __name__ == "__main__":
#     merge_chunks_in_folder()
