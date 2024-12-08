import ffmpeg
import platform
import whisper
import torch
import os
import argparse

# Check if a GPU is available
device = "cuda" if torch.cuda.is_available() else "cpu"

def get_ffmpeg_path():
    os_name = platform.system().lower()
    if os_name == "windows":
        return "./bin/ffmpeg.exe"
    # elif os_name == "linux":
    #     return "./bin/linux/ffmpeg"
    # elif os_name == "darwin":  # macOS
    #     return "./bin/macos/ffmpeg"
    else:
        raise Exception("Unsupported operating system")
    
def extract_audio(video_path, audio_path):
    ffmpeg_executable = get_ffmpeg_path()  # Path to local ffmpeg executable
    try:
        ffmpeg.input(video_path).output(audio_path, ac=1, ar=16000).run(cmd=ffmpeg_executable)
    except ffmpeg.Error as e:
        print(f"Error during audio extraction: {e}")
        raise

def transcribe_audio(audio_path):
    model = whisper.load_model("base",device=device)  # Choose model size: tiny, base, small, medium, large
    result = model.transcribe(audio_path)
    return result['text']

def transcribe_video(video_path):
    # Ensure the audio_dump directory exists
    dump_folder = "audio_dump"
    os.makedirs(dump_folder, exist_ok=True)
    # Extract the file name without extension and construct the audio path
    video_name = os.path.splitext(os.path.basename(video_path))[0]
    audio_path = os.path.join(dump_folder, f"{video_name}.wav")
    try:
        # Extract audio and transcribe it
        extract_audio(video_path, audio_path)
        transcription = transcribe_audio(audio_path)
    finally:
        # Delete the audio file after transcription
        if os.path.exists(audio_path):
            os.remove(audio_path)

    return transcription





if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Transcribe video to text.")
    parser.add_argument("video_path", help="Path to the video file")
    args = parser.parse_args()

    result = transcribe_video(args.video_path)
    print(result)