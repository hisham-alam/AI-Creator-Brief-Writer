"""
Transcriber module for converting video files to text using faster_whisper.
"""
import os
from pathlib import Path
from typing import Tuple, Optional

from faster_whisper import WhisperModel

from config import config


class Transcriber:
    """
    Class for transcribing video files to text using the faster_whisper model.
    """
    def __init__(self):
        """
        Initialize the transcriber with the model configuration from config.
        """
        print("Loading Whisper model...")
        self.model = WhisperModel(
            config.WHISPER_MODEL,
            device=config.WHISPER_DEVICE,
            compute_type=config.WHISPER_COMPUTE_TYPE
        )
        print(f"Model '{config.WHISPER_MODEL}' loaded successfully.")

    def transcribe_file(self, video_path: str) -> Tuple[str, Optional[str]]:
        """
        Transcribe a video file to text.
        
        Args:
            video_path: Path to the video file
            
        Returns:
            Tuple containing:
                - Full transcript text
                - Path to the saved transcript file, or None if saving failed
        """
        if not os.path.exists(video_path):
            print(f"Error: Video file not found at {video_path}")
            return "", None

        print(f"Transcribing: {os.path.basename(video_path)}")

        # Transcribe with settings that preserve casual speech
        segments, info = self.model.transcribe(
            video_path,
            beam_size=5,
            best_of=5,
            temperature=0.2,
            language="en",
            condition_on_previous_text=True,
            initial_prompt="Transcribe exactly as spoken, including casual speech like 'wanna', 'gonna', etc.",
            suppress_blank=False,
            word_timestamps=False
        )

        # Process segments and build transcript
        full_transcript = ""
        for segment in segments:
            print(f"[{segment.start:.2f}s -> {segment.end:.2f}s] {segment.text}")
            full_transcript += segment.text + " "
        
        full_transcript = full_transcript.strip()
        
        # Generate output file path based on input file
        video_basename = os.path.basename(video_path)
        video_name = os.path.splitext(video_basename)[0]
        output_file = os.path.join(config.TRANSCRIPT_DIR, f"{video_name}{config.TRANSCRIPT_EXTENSION}")
        
        try:
            # Ensure the directory exists
            os.makedirs(os.path.dirname(output_file), exist_ok=True)
            
            # Save the transcript
            with open(output_file, 'w') as f:
                f.write(full_transcript)
                
            print(f"Transcript saved to: {output_file}")
            return full_transcript, output_file
        except Exception as e:
            print(f"Error saving transcript: {str(e)}")
            return full_transcript, None


def transcribe_video(video_path: str) -> Tuple[str, Optional[str]]:
    """
    Convenience function to transcribe a video file.
    
    Args:
        video_path: Path to the video file
        
    Returns:
        Tuple containing:
            - Full transcript text
            - Path to the saved transcript file, or None if saving failed
    """
    transcriber = Transcriber()
    return transcriber.transcribe_file(video_path)