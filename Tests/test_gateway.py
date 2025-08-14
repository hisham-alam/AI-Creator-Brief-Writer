from wise_chain import load_model
import os

def test_video_processing_capability():
    """
    Test which models can actually process video files
    """
    print("=" * 60)
    print("Testing Video Processing Capabilities")
    print("=" * 60)
    print("\nTesting each model's ability to process video content...\n")
    
    # Video path
    video_path = "/Users/hisham.alam/Downloads/Coding Projects/Creator Briefs Automation/Ads/CMUS HackHiddenFees.mp4"
    
    # Check if video exists
    if os.path.exists(video_path):
        file_size = os.path.getsize(video_path) / (1024 * 1024)  # MB
        print(f"📹 Test video: CMUS HackHiddenFees.mp4 ({file_size:.2f} MB)")
    else:
        print(f"⚠️  Video file not found at: {video_path}")
    
    print("-" * 60)
    
    all_models = {
        "OpenAI": [
            "gpt-3.5-turbo", "gpt-4", "gpt-4-0125-preview", "gpt-4-turbo-preview",
            "gpt-4-turbo", "gpt-4o", "gpt-4o-mini", "o1-mini", "o1", "o1-preview"
        ],
        "Anthropic (Credal)": [
            "claude-3-haiku-20240307", "claude-3-5-haiku-latest", 
            "claude-3-opus-20240229", "claude-3-sonnet-20240229",
            "claude-3-5-sonnet-20240620", "claude-3-5-sonnet-latest"
        ],
        "Anthropic (Bedrock)": [
            "anthropic.claude-3-sonnet-20240229-v1:0",
            "anthropic.claude-v2:1", "anthropic.claude-instant-v1"
        ],
        "Amazon Bedrock": [
            "amazon.titan-tg1-large", "amazon.titan-text-express-v1"
        ],
        "VertexAI (Gemini)": [
            "gemini-2.5-flash", "gemini-2.5-pro",
            "gemini-2.0-flash-001", "gemini-2.0-flash-lite-001"
        ],
        "AI21": [
            "ai21.jamba-1-5-large-v1:0", "ai21.jamba-1-5-mini-v1:0"
        ]
    }
    
    video_capable = {}
    not_video_capable = {}
    failed_to_test = {}
    
    # Test prompts for video capability
    video_test_prompts = [
        "Can you analyze video files? Answer yes or no only.",
        "Do you have the ability to process video content including MP4 files? Answer yes or no.",
        "Can you watch and analyze videos? Just say yes or no."
    ]
    
    for vendor, models in all_models.items():
        print(f"\n📦 {vendor}")
        print("-" * 40)
        
        video_capable[vendor] = []
        not_video_capable[vendor] = []
        failed_to_test[vendor] = []
        
        for model_name in models:
            print(f"  {model_name[:35]:35s} ... ", end="")
            
            try:
                llm = load_model(
                    model_name,
                    team='ml-platform',
                    use_case='video-capability-test'
                )
                
                # Test 1: Direct question about video capability
                try:
                    response = llm.invoke(video_test_prompts[0]).strip().lower()
                    
                    if "yes" in response:
                        # Double-check with more specific question
                        response2 = llm.invoke(
                            "If I provide you with an MP4 video file, can you analyze its content, "
                            "including visual elements and speech? Answer yes or no."
                        ).strip().lower()
                        
                        if "yes" in response2:
                            print("✅ VIDEO CAPABLE")
                            video_capable[vendor].append(model_name)
                        else:
                            print("❌ No video support")
                            not_video_capable[vendor].append(model_name)
                    else:
                        print("❌ No video support")
                        not_video_capable[vendor].append(model_name)
                        
                except Exception as e:
                    error = str(e)
                    if "not yet supported" in error:
                        print("⚠️  Model not supported")
                    else:
                        print(f"⚠️  Error: {error[:20]}...")
                    failed_to_test[vendor].append((model_name, error[:50]))
                    
            except Exception as e:
                print(f"❌ Failed to load: {str(e)[:20]}...")
                failed_to_test[vendor].append((model_name, str(e)[:50]))
    
    # Summary
    print("\n" + "=" * 60)
    print("VIDEO CAPABILITY SUMMARY")
    print("=" * 60)
    
    print("\n✅ MODELS WITH VIDEO CAPABILITY:")
    print("-" * 40)
    total_video_capable = 0
    for vendor, models in video_capable.items():
        if models:
            print(f"\n{vendor}:")
            for model in models:
                print(f"  • {model}")
                total_video_capable += 1
    
    if total_video_capable == 0:
        print("\n  None found - models may not support direct video processing through this API")
    
    print(f"\n📊 Total video-capable models: {total_video_capable}")
    
    print("\n❌ MODELS WITHOUT VIDEO CAPABILITY:")
    print("-" * 40)
    for vendor, models in not_video_capable.items():
        if models:
            print(f"\n{vendor}:")
            for model in models:
                print(f"  • {model}")
    
    # Test actual video processing with claimed video-capable models
    if total_video_capable > 0:
        print("\n" + "=" * 60)
        print("TESTING ACTUAL VIDEO PROCESSING")
        print("=" * 60)
        print("\nLet's test if video-capable models can actually process a video file...")
        
        for vendor, models in video_capable.items():
            for model_name in models:
                print(f"\n🎬 Testing {model_name}:")
                try:
                    llm = load_model(model_name, team='ml-platform', use_case='video-test')
                    
                    # Try different approaches
                    test_prompts = [
                        f"Analyze this video file: {video_path}",
                        f"What can you tell me about the video at this path: {video_path}",
                        "I have a video file CMUS HackHiddenFees.mp4 about Wise. Can you analyze it?"
                    ]
                    
                    for prompt in test_prompts:
                        try:
                            print(f"  Trying: {prompt[:50]}...")
                            response = llm.invoke(prompt)
                            print(f"  Response: {response[:100]}...")
                            break
                        except Exception as e:
                            print(f"  Failed: {str(e)[:50]}...")
                            
                except Exception as e:
                    print(f"  Error loading model: {str(e)[:50]}...")
    
    # Save report
    with open("video_capability_report.txt", "w") as f:
        f.write("Video Processing Capability Report\n")
        f.write(f"Date: {__import__('datetime').datetime.now()}\n")
        f.write("=" * 60 + "\n\n")
        
        f.write("VIDEO-CAPABLE MODELS\n")
        f.write("-" * 40 + "\n")
        for vendor, models in video_capable.items():
            if models:
                f.write(f"\n{vendor}:\n")
                for model in models:
                    f.write(f"  ✅ {model}\n")
        
        f.write("\n\nNOT VIDEO-CAPABLE\n")
        f.write("-" * 40 + "\n")
        for vendor, models in not_video_capable.items():
            if models:
                f.write(f"\n{vendor}:\n")
                for model in models:
                    f.write(f"  ❌ {model}\n")
        
        f.write("\n\nFAILED TO TEST\n")
        f.write("-" * 40 + "\n")
        for vendor, models in failed_to_test.items():
            if models:
                f.write(f"\n{vendor}:\n")
                for model, error in models:
                    f.write(f"  ⚠️  {model}: {error}\n")
    
    print(f"\n📄 Report saved to 'video_capability_report.txt'")
    
    # Final recommendation
    print("\n" + "=" * 60)
    print("RECOMMENDATION")
    print("=" * 60)
    if total_video_capable == 0:
        print("\n⚠️  No models support direct video processing through the LLM Gateway.")
        print("\nAlternative approaches:")
        print("1. Extract frames from the video and analyze as images")
        print("2. Extract audio and transcribe separately")
        print("3. Use a video description in your prompt")
        print("4. Use external video analysis APIs and pass results to LLM")
    else:
        print(f"\n✅ Found {total_video_capable} model(s) with video capability")
        print("Note: Even if models claim video support, the LLM Gateway may not")
        print("support passing video files directly. You may need to use workarounds.")

if __name__ == "__main__":
    test_video_processing_capability()