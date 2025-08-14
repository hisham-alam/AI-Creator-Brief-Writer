from faster_whisper import WhisperModel
import os

video_path = "/Users/hisham.alam/Downloads/Coding Projects/Creator Briefs Automation/Ads/CMUS HackHiddenFees.mp4"

print("Loading model...")
model = WhisperModel("small", device="cpu", compute_type="int8")

print(f"Transcribing: {os.path.basename(video_path)}")

# Transcribe with settings that preserve casual speech
segments, info = model.transcribe(
    video_path,
    beam_size=5,
    best_of=5,
    temperature=0.2,
    language="en",
    condition_on_previous_text=True,
    initial_prompt="Transcribe exactly as spoken, including casual speech like 'wanna', 'gonna', etc.",  # Guide the model
    suppress_blank=False,  # Don't suppress informal tokens
    word_timestamps=False
)

full_transcript = ""
for segment in segments:
    print(f"[{segment.start:.2f}s -> {segment.end:.2f}s] {segment.text}")
    full_transcript += segment.text + " "

output_file = video_path.replace('.mp4', '_transcript.txt')
with open(output_file, 'w') as f:
    f.write(full_transcript.strip())

print(f"\n{'=' * 50}")
print(f"Transcript saved to: {output_file}")