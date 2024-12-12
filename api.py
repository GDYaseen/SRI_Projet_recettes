import sys
from flask import Flask, request, jsonify, send_from_directory
from retriever import preprocess_query, load_index_files, rank_documents
import os
from pypdf import PdfReader, PdfWriter
from PIL import Image
from PIL.PngImagePlugin import PngInfo
from inference import Inference
from video_transcriptor import transcribe_video, write_transcription_to_pdf

app = Flask(__name__)
inference = Inference()

# Path configurations
documents_path = "data/documents"
images_path = "data/img"
videos_path = "data/videos"

# Function to retrieve documents based on ranked_docs
def retrieve_documents(ranked_docs):
    results = []

    for doc_id in ranked_docs:
        document_found = False
        for filename in os.listdir(documents_path):
            if filename.endswith(".pdf"):
                file_path = os.path.join(documents_path, filename)

                # The title of the PDF is derived from its filename
                title = os.path.splitext(filename)[0]

                # Check if the document's metadata matches the given doc_id
                pdf_reader = PdfReader(file_path)
                metadata = pdf_reader.metadata
                if metadata.get("/indice_doc") == str(doc_id):
                    document_found = True

                    # Associate the document with its static image based on metadata
                    associated_image = None
                    for img_filename in os.listdir(images_path):
                        img_path = os.path.join(images_path, img_filename)
                        if img_filename.endswith(".jpg"):
                            with Image.open(img_path) as img:
                                metadata = PngInfo()
                                img_metadata = img.info
                                if img_metadata.get("img_id") == str(doc_id):
                                    associated_image = f"{images_path}/{img_filename}"
                                    break
                    
                    # Extract 150 characters from the document
                    extracted_text = ""
                    for page in pdf_reader.pages:
                        extracted_text += page.extract_text()
                        if len(extracted_text) >= 150:  # Stop once we have 150 characters
                            extracted_text = extracted_text[:150]
                            break
                    
                    # Clean up the text (optional, for better formatting)
                    extracted_text = extracted_text.replace("\n", " ").strip()

                    results.append({
                        "id": doc_id,
                        "title": title,
                        "image": associated_image,
                        "partOfText": extracted_text
                    })
                    break  # Move to the next document ID

        if not document_found:
            results.append({
                "id":None,
                "title": None,
                "image": None,
                "partOfText": None
            })

    return results

# Serve static files from the images folder
@app.route("/data/img/<path:filename>")
def serve_image(filename):
    return send_from_directory(images_path, filename)
# Serve static files from the images folder
@app.route("/data/videos/<path:filename>")
def serve_videos(filename):
    return send_from_directory(videos_path, filename)
@app.route("/data/documents/<path:filename>")
def serve_documents(filename):
    return send_from_directory(documents_path, filename)

# API endpoint to retrieve documents
@app.route("/api/search", methods=["GET"])
def search():
    data = request.get_json()
    query = data.get("query")
    if not query:
        return jsonify({"error": "Query is required."}), 400

    # File type filter: "doc", "vid", or "all"
    file_type = data.get("file_type", "all")

    results = {}

    if file_type in ("doc", "all"):
        # Process document search
        query_words = preprocess_query(query)
        doc_index_dir = './indexes/doc_indexes'
        doc_index_base = load_index_files(doc_index_dir, query_words)
        ranked_docs = rank_documents(query, doc_index_base)
        documents = retrieve_documents(ranked_docs)
        results["documents"] = documents

    if file_type in ("vid", "all"):
        # Process video search using semantic inference
        video_results = inference.llm_ans(query)
        results["videos"] = video_results

    if not results:
        return jsonify({"error": "Invalid file_type. Supported values are 'doc', 'vid', or 'all'."}), 400

    return results

# API endpoint to retrieve documents
@app.route("/api/details/<int:doc_id>", methods=["GET"])
def details(doc_id):
    if not doc_id:
        return jsonify({"error": "doc_id is required for text."}), 400
    
    # Process the document (text)
    for filename in os.listdir(documents_path):
        if filename.endswith(".pdf"):
            file_path = os.path.join(documents_path, filename)
            # Check if the document's metadata matches the given doc_id
            pdf_reader = PdfReader(file_path)
            metadata = pdf_reader.metadata
            if metadata.get("/indice_doc") == str(doc_id):
                associated_image = None
                for img_filename in os.listdir(images_path):
                    img_path = os.path.join(images_path, img_filename)
                    if img_filename.endswith(".jpg"):
                        with Image.open(img_path) as img:
                            img_metadata = img.info
                            if img_metadata.get("img_id") == str(doc_id):
                                associated_image = f"{images_path}/{img_filename}"
                                break
                # Extract text from the PDF
                text = ""
                for page in pdf_reader.pages:
                    text += page.extract_text()
                return jsonify({"id": doc_id, "text": text, "image": associated_image})
    return jsonify({"error": "Document not found."}), 404


if __name__ == "__main__":

    # if "re-vid" in sys.argv:
    #     # Get a list of all video files in the folder (only .mp4 files)
    #     video_files = [f for f in os.listdir(videos_path) if f.endswith(".mp4")]
    #     for video_file in video_files:
    #         video_path = os.path.join(videos_path, video_file)
    #         transcription = transcribe_video(video_path)
    #         # Extract the video name without extension
    #         video_name = os.path.splitext(os.path.basename(video_path))[0]
    #         # Write the transcription to a PDF
    #         write_transcription_to_pdf(transcription, video_name)
    
    app.run(debug=True,port=5009)
