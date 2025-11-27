"""
final_output.py

Simple RAG-style question-answering over your Sigma Web Dev course:

1. Load precomputed chunk embeddings from `final_embeddings.joblib`.
2. Ask the user for a question.
3. Embed the question using the same embedding model (bge-m3 via Ollama).
4. Find the top-k most similar chunks with cosine similarity.
5. Build a prompt for Llama (llama3.2 via Ollama) that:
   - Includes the most relevant chunks (with video number, title, timestamps).
   - Asks the model to guide the user to the correct video + timestamp.
6. Save the final prompt to `prompt.txt` and the model answer to `response.txt`.
"""

import numpy as np
from sklearn.metrics.pairwise import cosine_similarity
import joblib
import requests


def create_embedding(text_list):
    """
    Create embeddings for a list of texts using the bge-m3 model
    hosted on Ollama (http://localhost:11434/api/embed).
    """
    response = requests.post(
        "http://localhost:11434/api/embed",
        json={
            "model": "bge-m3",
            "input": text_list,
        },
    )
    embeddings = response.json()["embeddings"]
    return embeddings


def inference(prompt):
    """
    Call the Llama model (llama3.2) on Ollama and return the full JSON response.
    """
    response = requests.post(
        "http://localhost:11434/api/generate",
        json={
            "model": "llama3.2",
            "prompt": prompt,
            "stream": False,
        },
    )

    data = response.json()
    # Debug: print entire response JSON (can be commented out if noisy)
    print(data)
    return data


def main():
    # Load precomputed embeddings dataframe
    df = joblib.load("final_embeddings.joblib")

    # User query
    incoming_query = input("Ask a question: ")

    # Create embedding for the query
    question_embedding = create_embedding([incoming_query])[0]

    # Compute cosine similarity between query and all chunk embeddings
    similarities = cosine_similarity(
        np.vstack(df["embedding"]),
        [question_embedding],
    ).flatten()

    top_results = 3
    max_index = similarities.argsort()[::-1][:top_results]

    # Get top-k most similar chunks
    new_df = df.loc[max_index]

    # Build prompt for Llama
    prompt = f"""I am teaching web development in my Sigma web development course.
Here are video subtitle chunks containing:
- video number
- video title
- start time in seconds
- end time in seconds
- the text at that time

{new_df[["number", "title", "start", "end", "text"]].to_json(orient="records")}

---------------------------------
User question:
"{incoming_query}"

You are an assistant for this course. Based on the video chunks above, answer
in a human, conversational way. Clearly mention:
- in which video (by number and title)
- at what timestamps (start–end in seconds)
the relevant content is taught.

Guide the user to watch the correct part of the correct video.

If the user asks something unrelated to the course, say that you can only
answer questions related to the course.
"""

    # Save prompt for debugging / inspection
    with open("prompt.txt", "w", encoding="utf-8") as f:
        f.write(prompt)

    # Call Llama model
    response_json = inference(prompt)
    response_text = response_json["response"]

    # Print and save the final answer
    print("\n--- Model Response ---\n")
    print(response_text)

    with open("response.txt", "w", encoding="utf-8") as f:
        f.write(response_text)


if __name__ == "__main__":
    main()
