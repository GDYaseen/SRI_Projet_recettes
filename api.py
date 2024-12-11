from flask import Flask, request, jsonify, send_from_directory
from retriever import preprocess_query, load_index_files, rank_documents
import os
from pypdf import PdfReader, PdfWriter
from PIL import Image
from PIL.PngImagePlugin import PngInfo
app = Flask(__name__)

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

                    results.append({
                        "id": doc_id,
                        "title": title,
                        "image": associated_image
                    })
                    break  # Move to the next document ID

        if not document_found:
            results.append({
                "id":None,
                "title": None,
                "image": None
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
@app.route("/api/search", methods=["POST"])
def search():
    data = request.get_json()
    query = data.get("query")
    if not query:
        return jsonify({"error": "Query is required."}), 400

    # File type filter (not used for now as videos are not implemented yet)
    file_type = data.get("file_type", "all")

    # Use the ranking function from the retriever script
    query_words = preprocess_query(query)
    doc_index_dir = './indexes/doc_indexes'
    doc_index_base = load_index_files(doc_index_dir, query_words)
    ranked_docs = rank_documents(query, doc_index_base)

    # Retrieve documents based on ranked_docs
    documents = retrieve_documents(ranked_docs)

    return jsonify({"results": documents})

# API endpoint to retrieve documents
@app.route("/api/details/<int:doc_id>", methods=["GET"])
def details(doc_id):
    file_type = request.args.get("file_type")
    if not file_type:
        return jsonify({"error": "file_type is required."}), 400

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

                if file_type == "text":
                    # Extract text from the PDF
                    text = ""
                    for page in pdf_reader.pages:
                        text += page.extract_text()
                    return jsonify({"id":doc_id,"text": text, "image": associated_image})
                elif file_type == "vid":
                    # Construct video path
                    video_name = os.path.splitext(filename)[0] + ".mp4"
                    video_path = os.path.join(videos_path, video_name)
                    if os.path.exists(video_path):
                        return jsonify({"id":doc_id,"video": f"{videos_path}/{video_name}", "image": associated_image})
                    else:
                        return jsonify({"error": "Video not found."}), 404

    return jsonify({"error": "Document not found."}), 404

if __name__ == "__main__":
    app.run(debug=True,port=5009)
