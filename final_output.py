import numpy as np
from sklearn.metrics.pairwise import cosine_similarity
import joblib
import requests


def create_embedding(text_list):
    """
    Creating embeddings for a list of texts using the bge-m3 model
    hosted on Ollama's model.
    """
    response = requests.post(
        "http://localhost:11434/api/embed",
        json={
            "model": "bge-m3",
            "input": text_list,
        },
        timeout=300,
    )
    response.raise_for_status()
    # embeddings = response.json()["embeddings"]
    return response.json()["embeddings"]


def inference(prompt):
    """
    Calling an open-source model Llama(llama3.2) on Ollama and return the full JSON response.
    """
    response = requests.post(
        "http://localhost:11434/api/generate",
        json={
            "model": "llama3.2",
            "prompt": prompt,
            "stream": False,
        },
        timeout=300,
    )
    response.raise_for_status()
    # data = response.json()
    # print(data)
    return response.json()

def run_rag_query(top_k: int = 3) -> None:

    # Loading precomputed embeddings dataframe
    df = joblib.load("final_embeddings.joblib")
    
    # This is where User will raise a query
    incoming_query = input("Ask a question: ").strip()
    if not incoming_query:
        print("No question provided. Exiting.")
        return
    
    # Creating embedding for the query
    question_embedding = create_embedding([incoming_query])[0]
    
    # Computing cosine similarity between query and all chunk embeddings
    similarities = cosine_similarity(
        np.vstack(df["embedding"]),
        [question_embedding],
    ).flatten()
    
    top_indices = similarities.argsort()[::-1][:top_k]
    
    retrieved_df = df.loc[top_indices]
    
    # The Prompt
    prompt = f"""I am teaching web development in my Web development course.
Here are video subtitle chunks containing:
- video number
- video title
- start time in seconds
- end time in seconds
- the text at that time

{retrieved_df[["number", "title", "start", "end", "text"]].to_json(orient="records")}

-------------------------------------------------
User question:
"{incoming_query}"
User asked this question related to the video chunks, you have to answer in a human way (don't mention the above format, its just for you).
You are an assistant for this course. Based on the video chunks above, answer
in a human, conversational way. Clearly mention:
- in which video (by number and title)
- at what timestamps (start-end in seconds)
the relevant content is taught.

Guide the user to watch the correct part of the correct video.

If the user asks something unrelated to the course, say that you can only
answer questions related to the course.
"""

    # Saving the user's prompt for debugging and inspection
    with open("prompt.txt", "w", encoding="utf-8") as f:
        f.write(prompt)
    
    # Calling Llama model
    response_json = inference(prompt)
    response_text = response_json["response"]
    
    # Printing and save the final answer
    print("\n--- Model Response ---\n")
    print(response_text)
    
def main():
    run_rag_query()


if __name__ == "__main__":
    main()  
    






# def main():
#     # Loading precomputed embeddings dataframe
#     df = joblib.load("final_embeddings.joblib")

#     # This is where User will raise a query
#     incoming_query = input("Ask a question: ")

#     # Creating embedding for the query
#     question_embedding = create_embedding([incoming_query])[0]

#     # Computing cosine similarity between query and all chunk embeddings
#     similarities = cosine_similarity(
#         np.vstack(df["embedding"]),
#         [question_embedding],
#     ).flatten()

    
#     top_results = 3
#     max_index = similarities.argsort()[::-1][:top_results]

#     new_df = df.loc[max_index]

#     # The Prompt
#     prompt = f"""I am teaching web development in my Web development course.
# Here are video subtitle chunks containing:
# - video number
# - video title
# - start time in seconds
# - end time in seconds
# - the text at that time

# {retrieved_df[["number", "title", "start", "end", "text"]].to_json(orient="records")}

# -------------------------------------------------
# User question:
# "{incoming_query}"
# User asked this question related to the video chunks, you have to answer in a human way (don't mention the above format, its just for you).
# You are an assistant for this course. Based on the video chunks above, answer
# in a human, conversational way. Clearly mention:
# - in which video (by number and title)
# - at what timestamps (start-end in seconds)
# the relevant content is taught.

# Guide the user to watch the correct part of the correct video.

# If the user asks something unrelated to the course, say that you can only
# answer questions related to the course.
# """

#     # Saving the user's prompt for debugging and inspection
#     with open("prompt.txt", "w", encoding="utf-8") as f:
#         f.write(prompt)

#     # Calling Llama model
#     response_json = inference(prompt)
#     response_text = response_json["response"]

#     # Printing and save the final answer
#     print("\n--- Model Response ---\n")
#     print(response_text)

#     with open("response.txt", "w", encoding="utf-8") as f:
#         f.write(response_text)


# if __name__ == "__main__":
#     main()
#     run_rag_query()

