"""
File handler module for managing input/output operations.
"""
import os
from pathlib import Path
from typing import List, Dict, Optional, Tuple

from config import config


def get_video_files() -> List[str]:
    """
    Get all video files in the input directory.
    
    Returns:
        List of paths to video files
    """
    video_files = []
    
    for extension in config.SUPPORTED_VIDEO_EXTENSIONS:
        for file_path in Path(config.INPUT_DIR).glob(f"*{extension}"):
            video_files.append(str(file_path))
    
    return sorted(video_files)


def get_transcript_path(video_path: str) -> str:
    """
    Generate the transcript file path for a given video path.
    
    Args:
        video_path: Path to the video file
        
    Returns:
        Path to the transcript file
    """
    video_name = os.path.splitext(os.path.basename(video_path))[0]
    return os.path.join(config.TRANSCRIPT_DIR, f"{video_name}{config.TRANSCRIPT_EXTENSION}")


def get_brief_path(video_path: str) -> str:
    """
    Generate the brief file path for a given video path.
    
    Args:
        video_path: Path to the video file
        
    Returns:
        Path to the brief file
    """
    video_name = os.path.splitext(os.path.basename(video_path))[0]
    return os.path.join(config.BRIEF_DIR, f"{video_name}{config.BRIEF_EXTENSION}")


def get_processed_status() -> Dict[str, Dict[str, bool]]:
    """
    Get the processing status of all video files.
    
    Returns:
        Dictionary mapping video filenames to their processing status:
            {
                'video_name.mp4': {
                    'transcribed': True/False,
                    'brief_generated': True/False
                }
            }
    """
    status = {}
    
    # Get all video files
    video_files = get_video_files()
    
    for video_path in video_files:
        video_name = os.path.basename(video_path)
        transcript_path = get_transcript_path(video_path)
        brief_path = get_brief_path(video_path)
        
        status[video_name] = {
            'transcribed': os.path.exists(transcript_path),
            'brief_generated': os.path.exists(brief_path)
        }
    
    return status


def ensure_directories() -> None:
    """
    Ensure all necessary directories exist.
    """
    os.makedirs(config.INPUT_DIR, exist_ok=True)
    os.makedirs(config.TRANSCRIPT_DIR, exist_ok=True)
    os.makedirs(config.BRIEF_DIR, exist_ok=True)


def read_file(file_path: str) -> Optional[str]:
    """
    Read a file and return its contents.
    
    Args:
        file_path: Path to the file to read
        
    Returns:
        File contents as a string, or None if file doesn't exist
    """
    if not os.path.exists(file_path):
        return None
        
    with open(file_path, 'r') as f:
        return f.read()


def save_file(file_path: str, content: str) -> bool:
    """
    Save content to a file.
    
    Args:
        file_path: Path to save the file
        content: Content to write to the file
        
    Returns:
        True if successful, False otherwise
    """
    try:
        os.makedirs(os.path.dirname(file_path), exist_ok=True)
        with open(file_path, 'w') as f:
            f.write(content)
        return True
    except Exception as e:
        print(f"Error saving file to {file_path}: {str(e)}")
        return False