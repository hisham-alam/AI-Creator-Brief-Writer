"""
Configuration settings for the Creator Briefs Automation tool.
"""
import os
from pathlib import Path

# Base paths
BASE_DIR = Path(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
INPUT_DIR = BASE_DIR / "input" / "videos"
TRANSCRIPT_DIR = BASE_DIR / "output" / "transcripts"
BRIEF_DIR = BASE_DIR / "output" / "briefs"
SYSTEM_PROMPT_PATH = BASE_DIR / "config" / "system_prompt.txt"

# Ensure directories exist
INPUT_DIR.mkdir(exist_ok=True, parents=True)
TRANSCRIPT_DIR.mkdir(exist_ok=True, parents=True)
BRIEF_DIR.mkdir(exist_ok=True, parents=True)

# Whisper Model Configuration
WHISPER_MODEL = "small"  # Options: tiny, base, small, medium, large
WHISPER_DEVICE = "cpu"   # Options: cpu, cuda, auto
WHISPER_COMPUTE_TYPE = "int8"  # Options: float16, int8

# LLM Configuration
DEFAULT_LLM_MODEL = "claude-3-5-sonnet-latest"  # Default model to use for processing
LLM_TEAM = "marketing"  # Team identifier for LLM gateway
LLM_USE_CASE = "creator-briefs"  # Use case identifier for LLM gateway

# File extensions
SUPPORTED_VIDEO_EXTENSIONS = [".mp4", ".avi", ".mov", ".mkv", ".webm"]
TRANSCRIPT_EXTENSION = ".txt"
BRIEF_EXTENSION = ".md"