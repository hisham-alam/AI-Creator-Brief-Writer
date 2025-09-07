"""
Processor module for analyzing videos and generating content briefs using the LLM gateway.
With model fallback capability for multimodal models.
"""
import os
import time
import re
from typing import Optional, Tuple, Dict, Any, List

from wise_chain import load_model


# Default fallback models if not specified in config
DEFAULT_FALLBACK_MODELS = [
    "gemini-2.5-pro",
    "gemini-2.5-flash",
    "gemini-2.0-flash-001",
    "gemini-2.0-flash-lite-001",
    "anthropic.claude-3-sonnet-20240229-v1:0"
]


class Processor:
    """
    Class for analyzing videos and generating content briefs using multimodal LLM.
    Includes fallback mechanism if the primary model fails.
    """
    def __init__(self, config: Dict[str, Any], model_name: Optional[str] = None):
        """
        Initialize the processor with the specified model or default from config.
        
        Args:
            config: Configuration dictionary
            model_name: Name of the LLM model to use, defaults to config['DEFAULT_LLM_MODEL']
        """
        self.config = config
        self.primary_model_name = model_name or config['DEFAULT_LLM_MODEL']
        self._llm = None
        self._system_prompt = None
        self.working_model_name = None
    
    @property
    def llm(self):
        """
        Lazy loading of the LLM model with fallback mechanism.
        If the primary model fails, tries other models from the list.
        """
        if self._llm is None:
            # Try the primary model first
            self._llm = self._load_model_with_fallback()
            
        return self._llm
    
    def _load_model_with_fallback(self):
        """
        Try to load the primary model, and if that fails,
        try each model in the fallback list until one works.
        
        Returns:
            The loaded model
        """
        # Start with the primary model
        models_to_try = [self.primary_model_name]
        
        # Get fallback models from config or use defaults
        fallback_models = self.config.get('FALLBACK_MODELS', DEFAULT_FALLBACK_MODELS)
        
        # Add fallback models, avoiding duplicates
        for model in fallback_models:
            if model not in models_to_try:
                models_to_try.append(model)
        
        # Try each model in order
        for model_name in models_to_try:
            try:
                print(f"Trying to load model: {model_name}")
                model = load_model(
                    model_name,
                    team=self.config['LLM_TEAM'],
                    use_case=self.config['LLM_USE_CASE']
                )
                print(f"✅ Successfully loaded model: {model_name}")
                self.working_model_name = model_name
                return model
            except Exception as e:
                error_msg = str(e)
                print(f"❌ Failed to load model {model_name}: {error_msg}")
                # Brief pause before trying the next model
                time.sleep(0.5)
        
        # If we get here, all models failed
        raise RuntimeError(f"All multimodal models failed to load: Last error: {error_msg}")
        
    @property
    def system_prompt(self):
        """
        Load the system prompt from file.
        """
        if self._system_prompt is None:
            try:
                with open(self.config['SYSTEM_PROMPT_PATH'], 'r') as f:
                    self._system_prompt = f.read()
            except FileNotFoundError:
                print(f"System prompt file not found at {self.config['SYSTEM_PROMPT_PATH']}")
                self._system_prompt = "You are a professional content brief creator. Analyze the video and provide a comprehensive brief."
        return self._system_prompt

    def process_video(self, video_path: str) -> Tuple[str, Optional[str]]:
        """
        Process a video file and generate a content brief using multimodal capabilities.
        Includes robust error handling and model fallback.
        
        Args:
            video_path: Path to the video file
            
        Returns:
            Tuple containing:
                - Content brief text
                - Path to the saved brief file, or None if saving failed
        """
        video_name = os.path.splitext(os.path.basename(video_path))[0]
        print(f"Processing video: {video_name}")
        
        max_retries = 3
        for attempt in range(1, max_retries + 1):
            try:
                # Generate content brief by directly analyzing the video using the multimodal LLM
                print(f"Attempt {attempt}/{max_retries}: Analyzing video with model {self.working_model_name or self.primary_model_name}...")
                
                # Check which model we're using to determine the correct API format
                model_name = self.working_model_name or ""
                
                # Send the video file for analysis using the appropriate format
                if "gemini" in model_name.lower():
                    # Gemini format - include prompt as part of the user message
                    # The system prompt is included at the beginning of the message
                    prompt_instruction = (
                        f"{self.system_prompt}\n\n"
                        f"Please analyze the following video and create a comprehensive brief "
                        f"according to the instructions above. The video will be provided as the next input."
                    )
                    
                    print(f"Using Gemini multimodal format for {model_name}")
                    
                    try:
                        # This is the recommended format for Gemini 2.5 Pro
                        content_brief = self.llm.invoke(
                            [prompt_instruction, video_path]
                        )
                    except Exception as e:
                        if "Unknown field" in str(e) or "400" in str(e):
                            # Try alternative format if the first one fails
                            print("Gemini primary format failed, trying alternative format...")
                            content_brief = self.llm.invoke(
                                {"contents": [
                                    {"role": "user", "parts": [
                                        {"text": prompt_instruction}, 
                                        {"file_data": {"file_path": video_path}}
                                    ]}
                                ]}
                            )
                
                elif "claude" in model_name.lower():
                    # Claude format - uses system parameter
                    print(f"Using Claude format for {model_name}")
                    content_brief = self.llm.invoke(
                        video_path, 
                        system=self.system_prompt
                    )
                    
                else:
                    # Generic fallback - try both approaches
                    print(f"Using generic format for {model_name}")
                    try:
                        # Try with system parameter first
                        content_brief = self.llm.invoke(
                            video_path,
                            system=self.system_prompt
                        )
                    except Exception:
                        # If that fails, try with combined prompt
                        prompt = f"{self.system_prompt}\n\nPlease analyze this video:"
                        content_brief = self.llm.invoke(
                            [prompt, video_path]
                        )
                
                if not content_brief or len(content_brief.strip()) < 10:
                    print("Warning: Received empty or very short response. Retrying...")
                    continue
                
                # Extract the title from the content brief for the filename
                title = extract_title_from_brief(content_brief)
                
                # Use the extracted title or fallback to video filename
                file_title = title if title else video_name
                # Clean up the filename to avoid invalid characters
                safe_file_title = ''.join(c for c in file_title if c.isalnum() or c in ' -_()[]').strip()
                safe_file_title = safe_file_title.replace(' ', '_')
                
                # Generate output file path
                output_file = os.path.join(self.config['BRIEF_DIR'], f"{safe_file_title}{self.config['BRIEF_EXTENSION']}")
                
                # Save the brief
                os.makedirs(os.path.dirname(output_file), exist_ok=True)
                with open(output_file, 'w') as f:
                    f.write(content_brief)
                    
                print(f"Content brief successfully generated using model: {self.working_model_name}")
                print(f"Content brief saved to: {output_file}")
                return content_brief, output_file
                
            except Exception as e:
                error_msg = str(e)
                print(f"Error in attempt {attempt}/{max_retries}: {error_msg}")
                
                if attempt < max_retries:
                    # Different retry strategies based on error type
                    if "Unknown field for GenerationConfig: system" in error_msg:
                        print("Detected API incompatibility. Adjusting request format...")
                        # This will trigger different format on next attempt since is_gemini flag is already set
                    elif "rate limit" in error_msg.lower() or "quota" in error_msg.lower():
                        wait_time = min(attempt * 2, 10)  # Exponential backoff
                        print(f"Rate limit detected. Waiting {wait_time} seconds before retry...")
                        time.sleep(wait_time)
                    else:
                        print("Retrying with different parameters...")
                        time.sleep(1)  # Brief pause before retrying
                else:
                    print(f"All attempts failed. Last error: {error_msg}")
        
        # If we get here, all attempts failed
        raise RuntimeError(f"Failed to process video after {max_retries} attempts: {error_msg}")


def extract_title_from_brief(content_brief: str) -> Optional[str]:
    """
    Extract the title from the content brief.
    
    Args:
        content_brief: The content brief text
        
    Returns:
        The extracted title or None if not found
    """
    # Look for the video title in the brief using patterns:
    # Pattern 1: Ad [Number]: "[Video Title]" format
    title_pattern1 = re.search(r'Ad (?:.*?):\s*"([^"]+)"', content_brief)
    if title_pattern1:
        return title_pattern1.group(1)
    
    # Pattern 2: Video Title: "[Title]" format
    title_pattern2 = re.search(r'Video Title:\s*"([^"]+)"', content_brief)
    if title_pattern2:
        return title_pattern2.group(1)
    
    # Pattern 3: Any line containing "Title:" format
    title_pattern3 = re.search(r'(?:^|\n)\s*(?:Title|title):\s*"?([^"]*)"?', content_brief)
    if title_pattern3:
        return title_pattern3.group(1)
    
    return None


def process_video_file(video_path: str, config: Dict[str, Any], model_name: Optional[str] = None) -> Tuple[str, Optional[str]]:
    """
    Process a video file into a content brief.
    
    Args:
        video_path: Path to the video file
        config: Configuration dictionary
        model_name: Name of the LLM model to use, defaults to config['DEFAULT_LLM_MODEL']
        
    Returns:
        Tuple containing:
            - Content brief text
            - Path to the saved brief file, or None if saving failed
            
    Raises:
        FileNotFoundError: If the video file doesn't exist
        RuntimeError: If processing fails after multiple attempts
        ValueError: If the config is invalid
    """
    if not os.path.exists(video_path):
        raise FileNotFoundError(f"Video file not found at {video_path}")
    
    # Process the video directly
    try:
        processor = Processor(config, model_name)
        return processor.process_video(video_path)
    except Exception as e:
        # Re-raise the exception with context
        error_type = type(e).__name__
        error_msg = str(e)
        print(f"{error_type}: {error_msg}")
        raise