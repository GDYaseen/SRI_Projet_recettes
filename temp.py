import subprocess

result = subprocess.run(
    ["python", "video_transcriptor.py", "data/videos/La sauce au poivre.mp4"],
    capture_output=True,
    text=True
)
print(result.stdout)
#THIS IS A TESTING PROCESS FOR THE VIDEO TRANSCRIPTOR