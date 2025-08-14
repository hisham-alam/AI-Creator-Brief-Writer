"""
Processor module for generating content briefs from transcripts using the LLM gateway.
"""
import os
from pathlib import Path
from typing import Optional, Tuple

from wise_chain import load_model

from config import config


class Processor:
    """
    Class for processing transcripts into content briefs using LLM.
    """
    def __init__(self, model_name: Optional[str] = None):
        """
        Initialize the processor with the specified model or default from config.
        
        Args:
            model_name: Name of the LLM model to use, defaults to config.DEFAULT_LLM_MODEL
        """
        self.model_name = model_name or config.DEFAULT_LLM_MODEL
        self._llm = None
        self._system_prompt = None
    
    @property
    def llm(self):
        """
        Lazy loading of the LLM model.
        """
        if self._llm is None:
            print(f"Loading model: {self.model_name}")
            self._llm = load_model(
                self.model_name,
                team=config.LLM_TEAM,
                use_case=config.LLM_USE_CASE
            )
        return self._llm
        
    @property
    def system_prompt(self):
        """
        Load the system prompt from file.
        """
        if self._system_prompt is None:
            try:
                with open(config.SYSTEM_PROMPT_PATH, 'r') as f:
                    self._system_prompt = f.read()
            except FileNotFoundError:
                print(f"System prompt file not found at {config.SYSTEM_PROMPT_PATH}")
                self._system_prompt = "You are a professional content brief creator. Analyze the transcript and provide a comprehensive brief."
        return self._system_prompt

    def process_transcript(self, transcript_text: str, video_name: str) -> Tuple[str, Optional[str]]:
        """
        Process a transcript into a content brief.
        
        Args:
            transcript_text: The transcript text to process
            video_name: Name of the video file (without extension)
            
        Returns:
            Tuple containing:
                - Content brief text
                - Path to the saved brief file, or None if saving failed
        """
        print(f"Processing transcript for: {video_name}")
        
        # Prepare prompt with transcript
        user_prompt = f"""
Please analyze the following video transcript and create a content brief:

# TRANSCRIPT: {video_name}
{transcript_text}
"""
        
        try:
            # Generate content brief using the LLM
            print("Generating content brief...")
            content_brief = self.llm.invoke(user_prompt, system=self.system_prompt)
            
            # Generate output file path
            output_file = os.path.join(config.BRIEF_DIR, f"{video_name}{config.BRIEF_EXTENSION}")
            
            # Save the brief
            os.makedirs(os.path.dirname(output_file), exist_ok=True)
            with open(output_file, 'w') as f:
                f.write(content_brief)
                
            print(f"Content brief saved to: {output_file}")
            return content_brief, output_file
            
        except Exception as e:
            print(f"Error generating content brief: {str(e)}")
            return "", None


def process_transcript_file(transcript_path: str, model_name: Optional[str] = None) -> Tuple[str, Optional[str]]:
    """
    Process a transcript file into a content brief.
    
    Args:
        transcript_path: Path to the transcript file
        model_name: Name of the LLM model to use, defaults to config.DEFAULT_LLM_MODEL
        
    Returns:
        Tuple containing:
            - Content brief text
            - Path to the saved brief file, or None if saving failed
    """
    if not os.path.exists(transcript_path):
        print(f"Error: Transcript file not found at {transcript_path}")
        return "", None
    
    # Read transcript file
    with open(transcript_path, 'r') as f:
        transcript_text = f.read()
    
    # Get video name from transcript filename
    video_name = os.path.splitext(os.path.basename(transcript_path))[0]
    # Remove _transcript suffix if present
    if video_name.endswith("_transcript"):
        video_name = video_name[:-11]
    
    # Process the transcript
    processor = Processor(model_name)
    return processor.process_transcript(transcript_text, video_name)