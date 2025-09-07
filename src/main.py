#!/usr/bin/env python3
"""
Creator Briefs Automation Tool

This script automates the process of:
1. Analyzing all video files using Gemini 2.5 Pro to generate content briefs

Usage:
  python src/main.py

The script will automatically process all videos in the input directory.
"""
import os
import sys
import json
from pathlib import Path
from typing import List, Tuple, Optional, Dict, Any

# Add parent directory to sys.path to import from src
sys.path.insert(0, str(Path(__file__).parent.parent))
from src.processor import process_video_file
import src.file_handler as file_handler

# Load configuration from JSON
def load_config() -> Dict[str, Any]:
    """
    Load configuration from JSON and add dynamic paths.
    
    Returns:
        Dict containing the configuration settings
    """
    # Calculate base directory
    base_dir = Path(__file__).parent.parent
    
    # Load the JSON config
    config_path = base_dir / "config" / "config.json"
    with open(config_path, 'r') as f:
        config = json.load(f)
    
    # Calculate base directory
    base_dir = Path(__file__).parent.parent
    
    # Add dynamic paths
    config['PATHS'] = {
        'BASE_DIR': str(base_dir),
        'INPUT_DIR': os.path.expanduser(config.get('PATHS', {}).get('INPUT_DIR', '~/Downloads')),  # Use Downloads folder
        'BRIEF_DIR': str(base_dir / config.get('PATHS', {}).get('BRIEF_DIR', 'archive')),  # Use archive folder
        'SYSTEM_PROMPT_PATH': str(base_dir / "config" / "system_prompt.txt")
    }
    
    # Only ensure the output directory exists (we don't create Downloads folder)
    Path(config['PATHS']['BRIEF_DIR']).mkdir(exist_ok=True, parents=True)
    
    # Create a flat config dictionary for easier access
    flat_config = {}
    
    # Add paths
    for key, value in config['PATHS'].items():
        flat_config[key] = value
    
    # Add LLM config
    for key, value in config['LLM_CONFIG'].items():
        flat_config[key] = value
        
    # Specifically ensure FALLBACK_MODELS is included
    if 'FALLBACK_MODELS' in config['LLM_CONFIG']:
        flat_config['FALLBACK_MODELS'] = config['LLM_CONFIG']['FALLBACK_MODELS']
    
    # Add file extensions
    for key, value in config['FILE_EXTENSIONS'].items():
        flat_config[key] = value
    
    return flat_config

# Load configuration
config = load_config()


def process_video(video_path: str, config: Dict[str, Any], model_name: Optional[str] = None) -> bool:
    """
    Process a single video file.
    
    Args:
        video_path: Path to the video file
        config: Configuration dictionary
        model_name: Name of the LLM model to use
        
    Returns:
        True if processing was successful, False otherwise
    """
    print(f"\nProcessing video: {os.path.basename(video_path)}")
    print("-" * 60)
    
    try:
        # Process the video to generate a brief
        brief_text, saved_path = process_video_file(video_path, config, model_name)
        brief_success = saved_path is not None
        
        if brief_success:
            print(f"Successfully processed: {os.path.basename(video_path)}")
            print(f"Brief saved to: {saved_path}")
        
        return brief_success
        
    except FileNotFoundError as e:
        print(f"Error: {str(e)}")
        return False
    except RuntimeError as e:
        print(f"Processing error: {str(e)}")
        return False
    except Exception as e:
        # For unexpected errors, print the full error type and message
        error_type = type(e).__name__
        print(f"Unexpected error ({error_type}): {str(e)}")
        return False


def process_all_videos(config: Dict[str, Any]) -> Tuple[int, int]:
    """
    Process all video files in the input directory.
    
    Args:
        config: Configuration dictionary
        
    Returns:
        Tuple of (total_videos, successful_briefs)
    """
    print(f"\nProcessing all videos in: {config['INPUT_DIR']}")
    print("=" * 60)
    
    # Get all video files
    video_files = file_handler.get_video_files(config)
    
    if not video_files:
        print(f"No video files found in {config['INPUT_DIR']}")
        print(f"Supported extensions: {', '.join(config['SUPPORTED_VIDEO_EXTENSIONS'])}")
        return 0, 0
    
    # Process each video
    successful_briefs = 0
    
    for i, video_path in enumerate(video_files, 1):
        print(f"\nVideo {i}/{len(video_files)}: {os.path.basename(video_path)}")
        
        brief_success = process_video(
            video_path,
            config
        )
        
        if brief_success:
            successful_briefs += 1
    
    return len(video_files), successful_briefs


def main():
    """Main entry point."""
    try:
        # Load configuration
        config = load_config()
        
        # Display model information
        primary_model = config['DEFAULT_LLM_MODEL']
        fallback_models = config.get('FALLBACK_MODELS', [])
        
        # Ensure all directories exist
        file_handler.ensure_directories(config)
        
        print("\nCreator Briefs Automation Tool")
        print("=" * 60)
        print(f"Primary model: {primary_model}")
        print(f"Fallback models: {len(fallback_models)} configured")
        print("=" * 60)
        
        # Process all videos
        total, brief_count = process_all_videos(config)
        
        # Print summary
        print("\nSummary:")
        print("-" * 60)
        print(f"Total videos processed: {total}")
        print(f"Successful briefs: {brief_count}/{total}")
        
        print("\nDone!")
        
    except Exception as e:
        print(f"\n❌ Error: {str(e)}")
        print("\nTry running the test script to find working models:")
        print("  python -m src.test_models")
        sys.exit(1)


if __name__ == "__main__":
    main()