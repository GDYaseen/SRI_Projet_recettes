import os
import sys

from flask import app

from src.video_transcriptor import transcribe_video, write_transcription_to_pdf
from src.api import app

videos_path = "data/videos"

if __name__ == "__main__":

    if "re-transcript" in sys.argv:
        # Get a list of all video files in the folder (only .mp4 files)
        video_files = [f for f in os.listdir(videos_path) if f.endswith(".mp4")]
        for video_file in video_files:
            video_path = os.path.join(videos_path, video_file)
            transcription = transcribe_video(video_path)
            # Extract the video name without extension
            video_name = os.path.splitext(os.path.basename(video_path))[0]
            # Write the transcription to a PDF
            write_transcription_to_pdf(transcription, video_name)
        
        
    app.run(debug=False,port=5009)