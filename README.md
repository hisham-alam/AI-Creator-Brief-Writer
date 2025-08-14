# Creator Briefs Automation Tool

A powerful automation tool that transforms video content into detailed creator briefs using AI. This tool automatically transcribes videos and processes the transcripts to generate comprehensive content briefs for content creators.

## Features

- **Video Transcription**: Uses faster-whisper to generate accurate transcripts from video files
- **AI-Powered Brief Generation**: Processes transcripts using an LLM to create structured creator briefs
- **Batch Processing**: Process single videos or entire directories in one command
- **Customizable AI Model**: Flexibility to use different LLM models for brief generation
- **Organized File Management**: Maintains clear organization with separate directories for inputs and outputs

## Installation

### Requirements

- Python 3.8+
- FFmpeg (for audio extraction from videos)

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

3. Install FFmpeg if not already installed:

```bash
# macOS (using Homebrew)
brew install ffmpeg

# Ubuntu/Debian
sudo apt update && sudo apt install ffmpeg

# Windows (using Chocolatey)
choco install ffmpeg
```

## Directory Structure

```
creator_briefs_automation/
│
├── config/
│   ├── config.py           # Configuration settings
│   └── system_prompt.txt   # System prompt for AI
│
├── core/
│   ├── transcriber.py      # Video transcription functionality
│   └── processor.py        # Transcript processing and brief generation
│
├── utils/
│   └── file_handler.py     # File operations utilities
│
├── input/
│   └── videos/             # Place input videos here
│
├── output/
│   ├── transcripts/        # Generated transcripts
│   └── briefs/             # Generated creator briefs
│
├── main.py                 # Main script entry point
└── requirements.txt        # Project dependencies
```

## Usage

### Basic Commands

1. **Process all videos in the input directory**:

```bash
python main.py --all
```

2. **Process a specific video**:

```bash
python main.py --video path/to/video.mp4
```

3. **Only transcribe without generating briefs**:

```bash
python main.py --all --transcribe-only
```

4. **Use a specific LLM model**:

```bash
python main.py --all --model "claude-3-opus-20240229"
```

### Workflow

1. Place video files in the `input/videos/` directory
2. Run the script with your preferred options
3. Transcripts will be saved to `output/transcripts/`
4. Creator briefs will be saved to `output/briefs/`

## Configuration

The tool can be customized by modifying `config/config.py`:

- **Whisper Model Settings**: Change the model size, device, or compute type
- **LLM Configuration**: Set default model, team, and use case
- **File Paths**: Customize input/output directories
- **File Extensions**: Modify supported file extensions

## System Prompt Customization

The AI's behavior when creating briefs is controlled by the system prompt in `config/system_prompt.txt`. This can be modified to:

- Change the structure of generated briefs
- Focus on different aspects of content analysis
- Adjust the tone or format of the output

## Example Output

A typical creator brief includes:

- Video concept breakdown
- Full script with annotations
- Target audience analysis
- Hook ideas
- Key USPs
- Call-to-action recommendations
- Structure and format analysis

## Troubleshooting

- **FFmpeg Not Found**: Ensure FFmpeg is installed and in your system PATH
- **Video Not Found**: Verify file paths and permissions
- **LLM Authentication Issues**: Check your organization's API authentication requirements
- **Memory Issues**: For large videos, consider using a smaller Whisper model

## License

[Specify license information]

## Credits

- Built with [faster-whisper](https://github.com/guillaumekln/faster-whisper)
- Uses internal LLM gateway for brief generation

## Contributing

[Instructions for contributing to the project]