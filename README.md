# Creator Briefs Automation Tool

A powerful automation tool that transforms video content into detailed creator briefs using AI. This tool directly analyzes videos using Gemini 2.5 Pro's multimodal capabilities to generate comprehensive content briefs for content creators. The tool automatically extracts the video's title from the generated brief and uses it as the filename for the saved output.

## Features

- **Direct Video Analysis**: Uses Gemini 2.5 Pro to analyze video content directly (both visuals and audio)
- **AI-Powered Brief Generation**: Creates structured creator briefs with visual and content analysis
- **Smart File Naming**: Automatically names output files based on the extracted video title
- **Batch Processing**: Process single videos or entire directories in one command
- **Model Fallback System**: Automatically tries alternative LLM models if the primary model fails
- **Customizable AI Model**: Flexibility to use different LLM models for brief generation
- **Organized File Management**: Maintains clear organization with separate directories for inputs and outputs

## Installation

### Requirements

- Python 3.8+
- wise_chain library (for LLM integration)
- Internet connection (for LLM API access)

### Setup

1. Clone this repository:

```bash
git clone <repository-url>
cd creator-briefs-automation
```

2. Install dependencies:

```bash
pip install -r requirements.txt
```

## Directory Structure

```
creator_briefs_automation/
│
├── src/
│   ├── main.py             # Main script entry point
│   ├── processor.py        # Video processing and brief generation
│   └── file_handler.py     # File operations utilities
│
├── config/
│   ├── config.json         # Configuration settings in JSON format
│   └── system_prompt.txt   # System prompt for AI
│
├── archive/               # Default output directory for saved briefs
│
└── requirements.txt        # Project dependencies
```

## Usage

### Basic Commands

1. **Process all videos in the input directory**:

```bash
python src/main.py
```

The script automatically detects and processes all video files found in the configured input directory (defaults to ~/Downloads).

### Workflow

1. Place video files in your Downloads folder (or the configured input directory)
2. Run the script with `python src/main.py`
3. Creator briefs will be saved to the `archive` folder with filenames based on the extracted video titles
4. Each brief is saved as a separate text file named after the title extracted from its content

## Configuration

The tool is configured using `config/config.json`. Here's a detailed explanation of the configuration options:

```json
{
  "LLM_CONFIG": {
    "DEFAULT_LLM_MODEL": "gemini-2.5-pro",  // Primary model to use
    "LLM_TEAM": "your-team-name",          // Team name for API access
    "LLM_USE_CASE": "video-analysis",       // Use case identifier
    "FALLBACK_MODELS": [                    // Models to try if primary fails
      "claude-3-sonnet-20240229-v1:0"
    ]
  },
  "PATHS": {
    "INPUT_DIR": "~/Downloads",             // Where to look for videos
    "BRIEF_DIR": "archive"                  // Where to save output briefs
  },
  "FILE_EXTENSIONS": {
    "SUPPORTED_VIDEO_EXTENSIONS": [".mp4", ".mov", ".avi"],  // Video types
    "BRIEF_EXTENSION": ".txt"               // Output file extension
  }
}
```

### Configuration Options:

- **LLM Configuration**: 
  - `DEFAULT_LLM_MODEL`: The primary AI model to use
  - `LLM_TEAM` and `LLM_USE_CASE`: Organization-specific identifiers for API access
  - `FALLBACK_MODELS`: Ordered list of models to try if the primary model fails

- **File Paths**: 
  - `INPUT_DIR`: Directory to scan for videos (defaults to user's Downloads folder)
  - `BRIEF_DIR`: Where to save generated briefs

- **File Extensions**:
  - `SUPPORTED_VIDEO_EXTENSIONS`: List of video file types to process
  - `BRIEF_EXTENSION`: File extension for saved briefs

## System Prompt Customization

The AI's behavior when creating briefs is controlled by the system prompt in `config/system_prompt.txt`. This file contains detailed instructions that guide the AI in analyzing videos and structuring the output.

### Key Components of the System Prompt:

1. **Format Definition**: Provides the exact structure the AI should follow when creating briefs
2. **Analysis Instructions**: Directs the AI's focus to specific visual and content elements
3. **Output Guidelines**: Ensures the AI only outputs the brief itself with no additional commentary

You can modify this file to:

- Change the structure of generated briefs
- Focus on different aspects of content analysis
- Adjust the tone or format of the output
- Add or remove sections from the brief template

> **Note**: The system prompt includes specific instructions for the AI to output ONLY the brief content with no additional commentary or explanations.

## How It Works

### Core Components

1. **Video Processing Pipeline**:
   - The system scans the configured input directory for video files
   - Each video is processed individually through the `process_video` function
   - The video content is sent directly to the AI model for analysis

2. **AI Analysis**:
   - The system uses a multimodal LLM (like Gemini 2.5 Pro) capable of processing video
   - The AI analyzes both visual and audio content of the video
   - Analysis is guided by the system prompt that defines the output format

3. **Title Extraction**:
   - After receiving the AI's response, the system extracts the title using regex patterns
   - It looks for specific patterns like `Ad [Number]: "[Video Title]"` or `Video Title: "[Title]"`
   - The extracted title becomes the filename for the saved brief

4. **Model Fallback System**:
   - If the primary AI model fails, the system automatically tries alternative models
   - Models are tried in the order specified in the configuration
   - This ensures robust operation even if specific models are unavailable

5. **File Saving**:
   - The brief is saved as a text file named after the extracted title
   - If no title can be extracted, the original video filename is used
   - All special characters are removed to ensure valid filenames

### Example Output

A typical creator brief saved to the archive folder includes:

- Video concept breakdown with visual analysis
- Full script with annotations
- Visual elements description
- Target audience analysis
- Hook ideas
- Key USPs
- Call-to-action recommendations
- Structure and format analysis

## Troubleshooting

### Common Issues

- **Video Not Found**: 
  - Verify file paths and permissions
  - Check that the video format is in the supported extensions list
  - Make sure the input directory is correctly configured

- **LLM Authentication Issues**: 
  - Check your organization's API authentication requirements
  - Verify that the LLM_TEAM and LLM_USE_CASE values are correct
  - Ensure you have proper API access credentials

- **Video Processing Errors**: 
  - Check that video files are in supported formats
  - Ensure videos are not corrupted or excessively large
  - Look for error messages that indicate specific processing issues

- **All Models Failed**: 
  - This occurs when none of the models in the fallback list could be accessed
  - Check your internet connection and API access
  - Try adding additional models to the fallback list

### Error Messages

- **"All multimodal models failed to load"**: None of the specified models could be accessed
- **"Video file not found"**: The specified video path doesn't exist
- **"No video files found"**: No supported video formats were found in the input directory

## License

[Specify license information]

## Technical Details

### Key Files and Their Functions

1. **main.py**:
   - Entry point for the application
   - Manages the overall workflow and configuration
   - Provides user feedback and summary statistics

2. **processor.py**:
   - Contains the `Processor` class that handles video analysis
   - Implements the model fallback mechanism
   - Extracts titles from responses and handles file naming
   - Manages different API formats for various LLM models

3. **file_handler.py**:
   - Manages file system operations
   - Searches for video files in the input directory
   - Creates output directories and saves files

4. **config.json**:
   - Stores all configuration parameters
   - Defines model preferences and file paths
   - Lists supported file extensions

5. **system_prompt.txt**:
   - Contains instructions for the AI model
   - Defines the structure of the output brief
   - Ensures the AI provides only the requested content

### API Compatibility

The system is designed to work with multiple LLM APIs:

- **Gemini API**: Primary support for Google's Gemini models
- **Claude API**: Support for Anthropic's Claude models as fallbacks
- **Generic Fallback**: Alternative approaches for other API formats