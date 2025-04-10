import os
import cv2
import numpy as np
from flask import Flask, request, jsonify, send_from_directory
from werkzeug.utils import secure_filename

app = Flask(__name__)

UPLOAD_FOLDER = "uploads"
PROCESSED_FOLDER = "processed"

# Ensure directories exist
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
os.makedirs(PROCESSED_FOLDER, exist_ok=True)

app.config["UPLOAD_FOLDER"] = UPLOAD_FOLDER
app.config["PROCESSED_FOLDER"] = PROCESSED_FOLDER
app.config["ALLOWED_EXTENSIONS"] = {"png", "jpg", "jpeg"}

def allowed_file(filename):
    return "." in filename and filename.rsplit(".", 1)[1].lower() in app.config["ALLOWED_EXTENSIONS"]

def apply_watermark(image_path, watermark_text):
    image = cv2.imread(image_path)
    if image is None:
        return None  # Return None if the image couldn't be loaded

    h, w, _ = image.shape
    font = cv2.FONT_HERSHEY_SIMPLEX
    font_scale = min(w, h) / 1000
    thickness = 2

    text_size = cv2.getTextSize(watermark_text, font, font_scale, thickness)[0]
    text_x = (w - text_size[0]) // 2
    text_y = h - 50  # Position at the bottom

    cv2.putText(image, watermark_text, (text_x, text_y), font, font_scale, (255, 255, 255), thickness)

    processed_path = os.path.join(PROCESSED_FOLDER, "watermarked_" + os.path.basename(image_path))
    cv2.imwrite(processed_path, image)

    return processed_path

@app.route("/upload", methods=["POST"])
def upload_file():
    if "file" not in request.files:
        return jsonify({"error": "No file part"}), 400

    file = request.files["file"]
    watermark_text = request.form.get("watermark_text", "AUTHENTRACK")

    if file.filename == "":
        return jsonify({"error": "No selected file"}), 400

    if file and allowed_file(file.filename):
        filename = secure_filename(file.filename)
        file_path = os.path.join(app.config["UPLOAD_FOLDER"], filename)
        file.save(file_path)

        processed_path = apply_watermark(file_path, watermark_text)

        if processed_path:
            return jsonify({"download_url": f"http://127.0.0.1:5001/download/{os.path.basename(processed_path)}"}), 200
        else:
            return jsonify({"error": "Failed to process image"}), 500

    return jsonify({"error": "Invalid file type"}), 400

@app.route("/download/<filename>")
def download_file(filename):
    return send_from_directory(PROCESSED_FOLDER, filename)

if __name__ == "__main__":
    app.run(debug=True, port=5001)
