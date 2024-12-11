# import subprocess
# import os

# # Directory containing the video files
# video_folder = "data/videos"

# # Get a list of all video files in the folder (only .mp4 files in this case)
# video_files = [f for f in os.listdir(video_folder) if f.endswith(".mp4")]

# # Loop through each video file and run the transcription script
# for video_file in video_files:
#     video_path = os.path.join(video_folder, video_file)
    
#     # Run the transcription script on the video file
#     result = subprocess.run(
#         ["python", "video_transcriptor.py", video_path],
#         capture_output=True,
#         text=True
#     )
    
#     # Print the output (transcription) from the script
#     # print(f"Transcription for {video_file}:")
#     print(result.stdout)
#     print("-" * 50)  # Separator between transcriptions
#     print("\n")

import PyPDF2

def extract_text_from_pdf(pdf_path):
    # Open the PDF file
    with open(pdf_path, "rb") as file:
        # Create a PDF reader object
        reader = PyPDF2.PdfReader(file)
        
        # Extract text from each page
        text = ""
        for page_num in range(len(reader.pages)):
            page = reader.pages[page_num]
            text += page.extract_text()
        
    return text

if __name__ == "__main__":
    # Example PDF file path
    pdf_path = "🥔 Recette Savoureuse _ Gratin de Pommes de Terre au Bœuf Haché_transcription.pdf"  # Replace with the actual file path
    
    # Extract text from the PDF
    extracted_text = extract_text_from_pdf(pdf_path)
    
    # Print the extracted text
    print(extracted_text)
