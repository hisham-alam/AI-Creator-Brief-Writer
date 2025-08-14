#!/usr/bin/env python3
"""
Creator Briefs Automation Tool

This script automates the process of:
1. Transcribing video files to text using faster_whisper
2. Processing transcripts using an LLM to generate content briefs

Usage:
  python main.py [options]

Options:
  --video PATH        Process a specific video file
  --all               Process all video files in the input directory
  --model MODEL       Specify the LLM model to use for processing
  --transcribe-only   Only transcribe videos, don't generate briefs
  --help              Show this help message
"""
import os
import sys
import argparse
from typing import List, Tuple, Optional

from config import config
from core.transcriber import transcribe_video
from core.processor import process_transcript_file
from utils import file_handler


def parse_args():
    """Parse command line arguments."""
    parser = argparse.ArgumentParser(description='Creator Briefs Automation Tool')
    
    # Main operation options
    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument('--video', help='Process a specific video file')
    group.add_argument('--all', action='store_true', help='Process all video files in the input directory')
    
    # Additional options
    parser.add_argument('--model', help='Specify the LLM model to use for processing')
    parser.add_argument('--transcribe-only', action='store_true', help="Only transcribe videos, don't generate briefs")
    
    return parser.parse_args()


def process_video(video_path: str, model_name: Optional[str] = None, transcribe_only: bool = False) -> Tuple[bool, bool]:
    """
    Process a single video file.
    
    Args:
        video_path: Path to the video file
        model_name: Name of the LLM model to use
        transcribe_only: If True, only transcribe the video without generating a brief
        
    Returns:
        Tuple of (transcription_success, brief_success)
    """
    print(f"\nProcessing video: {os.path.basename(video_path)}")
    print("-" * 60)
    
    # Check if the file exists
    if not os.path.exists(video_path):
        print(f"Error: Video file not found at {video_path}")
        return False, False
    
    # Check if the transcript already exists
    transcript_path = file_handler.get_transcript_path(video_path)
    transcript_exists = os.path.exists(transcript_path)
    
    if transcript_exists:
        print(f"Transcript already exists at: {transcript_path}")
        transcript_text = file_handler.read_file(transcript_path)
        transcription_success = True
    else:
        # Transcribe the video
        transcript_text, saved_path = transcribe_video(video_path)
        transcription_success = saved_path is not None
    
    # If transcribe-only flag is set or transcription failed, stop here
    if transcribe_only or not transcription_success:
        return transcription_success, False
    
    # Process the transcript to generate a brief
    brief_text, saved_path = process_transcript_file(transcript_path, model_name)
    brief_success = saved_path is not None
    
    return transcription_success, brief_success


def process_all_videos(model_name: Optional[str] = None, transcribe_only: bool = False) -> Tuple[int, int, int]:
    """
    Process all video files in the input directory.
    
    Args:
        model_name: Name of the LLM model to use
        transcribe_only: If True, only transcribe videos without generating briefs
        
    Returns:
        Tuple of (total_videos, successful_transcriptions, successful_briefs)
    """
    print(f"\nProcessing all videos in: {config.INPUT_DIR}")
    print("=" * 60)
    
    # Get all video files
    video_files = file_handler.get_video_files()
    
    if not video_files:
        print(f"No video files found in {config.INPUT_DIR}")
        print(f"Supported extensions: {', '.join(config.SUPPORTED_VIDEO_EXTENSIONS)}")
        return 0, 0, 0
    
    # Process each video
    successful_transcriptions = 0
    successful_briefs = 0
    
    for i, video_path in enumerate(video_files, 1):
        print(f"\nVideo {i}/{len(video_files)}: {os.path.basename(video_path)}")
        
        trans_success, brief_success = process_video(
            video_path, 
            model_name=model_name,
            transcribe_only=transcribe_only
        )
        
        if trans_success:
            successful_transcriptions += 1
        if brief_success:
            successful_briefs += 1
    
    return len(video_files), successful_transcriptions, successful_briefs


def main():
    """Main entry point."""
    # Parse command line arguments
    args = parse_args()
    
    # Ensure all directories exist
    file_handler.ensure_directories()
    
    print("\nCreator Briefs Automation Tool")
    print("=" * 60)
    
    if args.all:
        # Process all videos
        total, trans_count, brief_count = process_all_videos(
            model_name=args.model,
            transcribe_only=args.transcribe_only
        )
        
        # Print summary
        print("\nSummary:")
        print("-" * 60)
        print(f"Total videos processed: {total}")
        print(f"Successful transcriptions: {trans_count}/{total}")
        
        if not args.transcribe_only:
            print(f"Successful briefs: {brief_count}/{total}")
    else:
        # Process a specific video
        if not os.path.exists(args.video):
            print(f"Error: Video file not found at {args.video}")
            sys.exit(1)
            
        trans_success, brief_success = process_video(
            args.video, 
            model_name=args.model,
            transcribe_only=args.transcribe_only
        )
        
        # Print summary
        print("\nSummary:")
        print("-" * 60)
        print(f"Transcription: {'Success' if trans_success else 'Failed'}")
        
        if not args.transcribe_only:
            print(f"Brief generation: {'Success' if brief_success else 'Failed'}")
    
    print("\nDone!")


if __name__ == "__main__":
    main()