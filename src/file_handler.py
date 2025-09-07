"""
File handler module for managing input/output operations.
"""
import os
import sys
from pathlib import Path
from typing import List, Dict, Optional

# Importing config happens in main.py, and is passed to this module


def get_video_files(config) -> List[str]:
    """
    Get all video files in the input directory (Downloads folder) and its subfolders.
    
    Args:
        config: Configuration dictionary
        
    Returns:
        List of paths to video files
    """
    video_files = []
    
    # Expand ~ to user's home directory if present
    input_dir = os.path.expanduser(config['INPUT_DIR'])
    
    # Search for video files in Downloads folder and its subfolders
    for extension in config['SUPPORTED_VIDEO_EXTENSIONS']:
        for file_path in Path(input_dir).glob(f"**/*{extension}"):
            video_files.append(str(file_path))
    
    print(f"Found {len(video_files)} video file(s) in {input_dir} and its subfolders")
    return sorted(video_files)


def get_brief_path(video_path: str, config) -> str:
    """
    Generate the brief file path for a given video path.
    Preserves any folder structure from the Downloads path.
    
    Args:
        video_path: Path to the video file
        config: Configuration dictionary
        
    Returns:
        Path to the brief file
    """
    video_name = os.path.splitext(os.path.basename(video_path))[0]
    return os.path.join(config['BRIEF_DIR'], f"{video_name}{config['BRIEF_EXTENSION']}")



def get_processing_status(config) -> Dict[str, bool]:
    """
    Get the processing status of all video files.
    
    Args:
        config: Configuration dictionary
    
    Returns:
        Dictionary mapping video filenames to their processing status:
            {
                'video_name.mp4': True/False
            }
    """
    status = {}
    
    # Get all video files
    video_files = get_video_files(config)
    
    for video_path in video_files:
        video_name = os.path.basename(video_path)
        brief_path = get_brief_path(video_path, config)
        
        status[video_name] = os.path.exists(brief_path)
    
    return status


def ensure_directories(config) -> None:
    """
    Ensure all necessary directories exist.
    
    Args:
        config: Configuration dictionary
    """
    # We don't create the INPUT_DIR (Downloads folder) as it should already exist
    os.makedirs(config['BRIEF_DIR'], exist_ok=True)


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