import cv2
import numpy as np
import os
from flask import Flask, request, jsonify, send_from_directory
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

# Function to embed watermark using DCT
def embed_watermark(image_path, watermark_text):
    img = cv2.imread(image_path, cv2.IMREAD_GRAYSCALE)
    if img is None:
        return None  # Handle error if image is not read properly

    h, w = img.shape
    
    # Apply DCT
    dct_img = cv2.dct(np.float32(img))
    
    # Embed watermark text into DCT coefficients
    watermark_binary = ''.join(format(ord(c), '08b') for c in watermark_text)
    idx = 0
    for i in range(10, 50):
        for j in range(10, 50):
            if idx < len(watermark_binary):
                dct_img[i, j] += int(watermark_binary[idx]) * 0.1  # Small change to avoid distortion
                idx += 1
    
    # Apply inverse DCT
    watermarked_img = cv2.idct(dct_img)
    watermarked_img = np.clip(watermarked_img, 0, 255).astype(np.uint8)
    
    output_path = "watermarked_image.png"
    cv2.imwrite(output_path, watermarked_img)
    
    return output_path

# Function to extract watermark from image
def extract_watermark(image_path):
    img = cv2.imread(image_path, cv2.IMREAD_GRAYSCALE)
    if img is None:
        return None  # Handle error if image is not read properly
    
    dct_img = cv2.dct(np.float32(img))
    
    binary_string = ""
    for i in range(10, 50):
        for j in range(10, 50):
            binary_string += '1' if dct_img[i, j] > 0 else '0'
    
    extracted_text = "".join(chr(int(binary_string[i:i+8], 2)) for i in range(0, len(binary_string), 8))
    return extracted_text.strip()

# API to embed watermark in an image
@app.route('/watermark/image/embed', methods=['POST'])
def embed_image_watermark():
    if 'image' not in request.files:
        return jsonify({"error": "No image uploaded"}), 400

    file = request.files['image']
    watermark_text = request.form.get('watermark', '')

    if not watermark_text:
        return jsonify({"error": "Watermark text is required"}), 400

    image_path = "input_image.png"
    file.save(image_path)

    watermarked_image_path = embed_watermark(image_path, watermark_text)
    if not watermarked_image_path:
        return jsonify({"error": "Failed to process image"}), 500

    return jsonify({"watermarked_image": "http://127.0.0.1:5001/watermarked_image.png"})

# API to extract watermark from an image
@app.route('/watermark/image/extract', methods=['POST'])
def extract_image_watermark():
    if 'image' not in request.files:
        return jsonify({"error": "No image uploaded"}), 400

    file = request.files['image']
    image_path = "uploaded_image.png"
    file.save(image_path)

    extracted_text = extract_watermark(image_path)
    if extracted_text is None:
        return jsonify({"error": "Failed to extract watermark"}), 500

    return jsonify({"extracted_watermark": extracted_text})

# API to serve the watermarked image
@app.route('/watermarked_image.png')
def get_watermarked_image():
    return send_from_directory(os.getcwd(), "watermarked_image.png", mimetype="image/png")

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5001)
