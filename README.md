# Your anytime anywhere deployable - RAG Assistant is HERE

Hello everyone 
Welcome to this project — a fully local **Retrieval-Augmented Generation (RAG) Assistant** designed for the **Web Development Course**.

This system can **understand your question**, find **exact video segments** (video number + timestamps), and answer using a **local LLM** running on your machine.  
Everything is done using a **self-built pipeline** involving Whisper, ffmpeg, Cosine Similarity, Embeddings, and Ollama.

---

## Features

- Automatically extracts audio from lecture videos  
- Whisper-based transcription (Hindi → English translation)  
- Subtitle chunk creation & merging  
- High-quality embeddings using **bge-m3** (via Ollama)  
- Semantic search using **cosine similarity**  
- Llama 3.2 powered answer generation  
- Complete offline pipeline — *no API keys needed*  
- Points you to the **correct video + timestamp** where the concept is explained  

---

##  Project Structure
So , This is how I have structured the project :
```
├── 01_videos_processing.py # Rename videos and extracts audio
├── 02_mp3_to_json.py # Convert audio to whisper transcripts
├── 03_merge_chunks.py # Merge small subtitle chunks
├── 04_preprocess_jsons.py # Generate embeddings for each chunk
├── 05_final_output.py # Question answering system
├── video/ # raw .mp4 videos
├── final_videos/ # Clean renamed videos
├── final_audios/ # Extracted .mp3 files
├── new_jsons/ # Whisper transcription outputs
├── final_jsons/ # Merged subtitle chunks
├── final_embeddings.joblib # Embeddings DataFrame
├── prompt.txt # Saved prompt sent to Llama
├── response.txt # Model’s final answer
├── requirements.txt
└── README.md

To begin , you need to install all the necessary dependencies:

Install required dependencies using:

     pip install -r requirements.txt

You must install:
    ffmpeg
    Ollama

Then pull the required models in Ollama:
    ollama pull bge-m3
    ollama pull llama3.2

```  
## Here's how you can run

Follow these steps exactly:

## 1)Process raw videos

Renames messy video titles and extracts audio:
```bash
python 01_videos_processing.py
```

## 2)Convert audio to subtitles

Uses Whisper for transcription (Hindi → English):
```bash
python 02_mp3_to_json.py
```

## 3)Merge subtitle chunks

Creates cleaner, bigger chunks of text:
```bash
python 03_merge_chunks.py
```

## 4)Generate embeddings

Creates embeddings using bge-m3 and stores them:
```bash
python 04_preprocess_jsons.py
```
This generates:                
               final_embeddings.joblib

## 5)Run the Question-Answering System

Ask any question from your Web Development course:
```bash
python 05_final_output.py
```
You will get:

A human-like explanation

Video number  

Start & end timestamps

Direct reference to where the concept is taught

## How this workflow works

Video to Audio extraction (ffmpeg)

Audio to Text conversion (Whisper medium)

Subtitle chunks to Merged chunks

Embeddings created using bge-m3

User query gets Embedded & matched using cosine similarity

Top 3 relevant text chunks are extracted

Llama 3.2 generates a human answer with timestamps


## Models Used

Whisper (medium) – transcription + Hindi → English translation

bge-m3 – embedding model (via Ollama)

Llama 3.2 – LLM for final answer generation

## Example Use Case
```bash
Ask a question: "Where is float & clear taught in this course"
```
RESULT:

```bash
Hello! I see you're asking about where float and clear are taught in this course. The relevant content is actually covered in Video 34: "CSS Float & Clear".

The explanation of how float and clear work starts around 35.4 seconds into that video, and continues until 62.38 seconds. You can easily find those timestamps on the video.

If you want to get a better understanding of both concepts, the instructor also explains that if you're using both float and clear, you'll need to use "clear both" to avoid any overlap or other issues, starting at around 397.8-407.8 seconds into Video 34.

So, I'd recommend checking out those timestamps in Video 34: "CSS Float & Clear".
```
## Contact

For suggestions, improvements, or issues, feel free to open a GitHub issue.
