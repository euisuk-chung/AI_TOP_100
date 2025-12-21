"""
Q8 인수인계 - Whisper 음성 전사 스크립트
"""
import os
from pathlib import Path
import torch
import whisper

BASE_DIR = Path(__file__).parent
AUDIO_DIR = BASE_DIR / "5_통화" / "5_통화"
OUTPUT_DIR = BASE_DIR / "transcripts"

def main():
    OUTPUT_DIR.mkdir(exist_ok=True)

    # Load model on CPU to avoid CUDA compatibility issues
    print("Loading Whisper model (base) on CPU...")
    model = whisper.load_model("base", device="cpu")

    # Find all audio files
    audio_files = sorted(AUDIO_DIR.glob("*.m4a"))
    print(f"Found {len(audio_files)} audio files\n")

    for audio_file in audio_files:
        print(f"Transcribing: {audio_file.name}...")

        # Transcribe
        result = model.transcribe(str(audio_file), language='ko')

        # Save transcript
        output_file = OUTPUT_DIR / f"{audio_file.stem}.txt"
        with open(output_file, 'w', encoding='utf-8') as f:
            f.write(result['text'])

        print(f"  -> {output_file.name}")
        print(f"  Text: {result['text'][:200]}...\n")

    print("Done!")


if __name__ == "__main__":
    main()
