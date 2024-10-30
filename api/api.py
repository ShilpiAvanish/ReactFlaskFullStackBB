from flask import Flask, request, jsonify
from flask_cors import CORS
import os
import fitz  # PyMuPDF
import re

app = Flask(__name__)
CORS(app)

UPLOAD_FOLDER = "uploads"
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
app.config["UPLOAD_FOLDER"] = UPLOAD_FOLDER

def extract_five_digit_numbers(file_path):
    five_digit_numbers = []
    with fitz.open(file_path) as pdf_document:
        for page_num in range(pdf_document.page_count):
            page_text = pdf_document.load_page(page_num).get_text("text")
            five_digit_numbers += re.findall(r'\b\d{5}\b', page_text)
    return five_digit_numbers

@app.route("/upload", methods=["POST"])
def upload_file():
    if "file" not in request.files:
        return jsonify({"error": "No file part"}), 400

    file = request.files["file"]
    if file.filename == "":
        return jsonify({"error": "No selected file"}), 400

    file_path = os.path.join(app.config["UPLOAD_FOLDER"], file.filename)
    file.save(file_path)

    # Extract five-digit numbers from the PDF file
    try:
        five_digit_numbers = extract_five_digit_numbers(file_path)
        return jsonify({
            "message": "File uploaded and processed successfully",
            "five_digit_numbers": five_digit_numbers
        }), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == "__main__":
    app.run(debug=True)
