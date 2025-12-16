import json
import os
import requests
import pandas as pd
import joblib
from sklearn.metrics.pairwise import cosine_similarity


def create_embedding(text_list):
    """
    Here, We are sending a list of text strings to Ollama's embedding endpoint and returns a list of embedding vectors.
    """
    response = requests.post(
        "http://localhost:11434/api/embed",
        json={
            "model": "bge-m3",
            "input": text_list
        }
    )
    return response.json()["embeddings"]


def process_json_files(input_folder: str = "final_jsons",
                    output_file: str = "final_embeddings.joblib") -> None:
    """
    Converting all JSON chunk files into a consolidated DataFrame
    containing chunk metadata and embeddings.
    """
    json_files = os.listdir(input_folder)
    all_chunks = []
    chunk_id = 0

    for file_name in json_files:
        if not file_name.endswith(".json"):
            continue

        file_path = os.path.join(input_folder, file_name)

        with open(file_path, "r", encoding="utf-8") as f:
            content = json.load(f)

        print(f"Creating embeddings for {file_name}")

        # Creating embeddings in batch for all text inside this JSON
        embeddings = create_embedding([c["text"] for c in content["chunks"]])

        # Attaching metadata ,embeddings, unique chunk ID
        for i, chunk in enumerate(content["chunks"]):
            chunk["chunk_id"] = chunk_id
            chunk["embedding"] = embeddings[i]
            chunk_id += 1

            all_chunks.append(chunk)

    # Converting list of dicts into DataFrame
    df = pd.DataFrame.from_records(all_chunks)

    # Saving embeddings dataframe
    joblib.dump(df, output_file)
    print(f"\nSaved final embeddings to: {output_file}")


if __name__ == "__main__":
    process_json_files()
