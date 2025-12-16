"""
Here I have combined all the previous .py files to be executed just by one .py file
This is the final pipeline Runner for RAG Assistant

This script runs the complete end-to-end RAG pipeline in sequence:

1. Video preprocessing (rename + audio extraction)
2. Audio transcription (Whisper)
3. Chunk merging
4. Embedding generation
5. RAG-based question answering

Run with:
    python main.py
"""

import sys
import time

import videos_processing
import mp3_to_json
import merge_chunks
import preprocess_jsons
import final_output


def run_step(step_name: str, step_func):

    print("=" * 60)
    print(f" {step_name}")
    print("=" * 60)

    start_time = time.time()
    try:
        step_func()
    except Exception as e:
        print(f"\n Error during step: {step_name}")
        print(f"Reason: {e}")
        sys.exit(1)

    elapsed = time.time() - start_time
    print(f" Completed: {step_name} (took {elapsed:.2f} seconds)\n")


def main():
    print("\n Starting RAG Assistant Full Pipeline\n")

    # STEP 1: Video preprocessing + audio extraction
    run_step(
        "Video preprocessing & audio extraction",
        videos_processing.main,
    )

    # STEP 2: Audio → JSON transcription
    run_step(
        "Audio transcription (Whisper)",
        mp3_to_json.main,
    )

    # STEP 3: Merge subtitle chunks
    run_step(
        "Chunk merging",
        merge_chunks.main,
    )

    # STEP 4: Generate embeddings
    run_step(
        "Embedding generation",
        preprocess_jsons.main,
    )

    # STEP 5: RAG inference
    run_step(
        "RAG question answering",
        final_output.main,
    )

    print("\nRAG Assistant Pipeline Completed Successfully!")


if __name__ == "__main__":
    main()
