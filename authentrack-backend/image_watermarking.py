import cv2
import numpy as np
import os
import hashlib
from flask import Flask, request, jsonify, send_from_directory
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

UPLOAD_FOLDER = "uploads"
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

def compute_hash(image_path):
    with open(image_path, "rb") as f:
        return hashlib.sha256(f.read()).hexdigest()

def embed_watermark(image_path, watermark_text="AuthenTrack"):
    img = cv2.imread(image_path, cv2.IMREAD_GRAYSCALE)
    if img is None:
        return None, None, "Error reading image."

    h, w = img.shape
    dct_img = cv2.dct(np.float32(img))

    watermark_bin = ''.join(format(ord(char), '08b') for char in watermark_text)
    flat_dct = dct_img.flatten()

    for i, bit in enumerate(watermark_bin):
        flat_dct[i] = flat_dct[i] + 1 if bit == '1' else flat_dct[i] - 1

    watermarked_dct = flat_dct.reshape(dct_img.shape)
    watermarked_img = cv2.idct(watermarked_dct)
    watermarked_img = np.clip(watermarked_img, 0, 255).astype(np.uint8)

    output_path = os.path.join(UPLOAD_FOLDER, "watermarked.png")
    cv2.imwrite(output_path, watermarked_img)
    return output_path, compute_hash(output_path), None

@app.route("/upload-image", methods=["POST"])
def upload_image():
    if "image" not in request.files:
        return jsonify({"error": "No image uploaded"}), 400

    file = request.files["image"]
    filename = file.filename
    input_path = os.path.join(UPLOAD_FOLDER, filename)
    file.save(input_path)

    watermarked_path, image_hash, error = embed_watermark(input_path)

    if error:
        return jsonify({"error": error}), 500

    return jsonify({
        "message": "Watermark embedded",
        "image_url": f"http://127.0.0.1:5001/{watermarked_path}",
        "image_hash": image_hash
    })

@app.route("/check-tamper", methods=["POST"])
def check_tamper():
    if "image" not in request.files or "original_hash" not in request.form:
        return jsonify({"error": "Missing data"}), 400

    file = request.files["image"]
    original_hash = request.form["original_hash"]

    file_path = os.path.join(UPLOAD_FOLDER, "uploaded_check.png")
    file.save(file_path)

    new_hash = compute_hash(file_path)
    tampered = new_hash != original_hash

    return jsonify({
        "tampered": tampered,
        "new_hash": new_hash,
        "original_hash": original_hash
    })

@app.route("/uploads/<filename>")
def serve_image(filename):
    return send_from_directory(UPLOAD_FOLDER, filename)

if __name__ == "__main__":
    app.run(debug=True, port=5001)
