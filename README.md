# RAG Assistant 

This project is an end-to-end RAG-style system built on local models (Whisper + Ollama) to answer questions from the Sigma Web Development Course. It extracts subtitles from videos, creates embeddings, and uses a local LLM to answer user queries with timestamps.

---

##  Features
- Convert video → audio → subtitles → text chunks  
- Whisper transcription (Hindi → English translation)  
- Chunk merging & embedding using `bge-m3`  
- Similarity search using cosine similarity  
- Local LLM answering with video timestamps (Llama 3.2 via Ollama)  
- Completely offline, no API keys needed  

---

##  Project Structure

