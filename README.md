# 🔒 AuthenTrack: AI-Persistent Watermarking & Tamper Detection System

AuthenTrack is a web-based application that provides AI-Persistent watermarking and tamper detection for digital images. Built during my internship at [Stuvaly Technology](https://www.linkedin.com/company/stuvaly/), this tool ensures content authenticity by embedding invisible watermarks using DCT (Discrete Cosine Transform) and detecting unauthorized alterations in images.

## Features

-  **Invisible Watermarking**: Embed imperceptible watermarks in the image’s frequency domain using DCT.
-  **Tamper Detection**: Detect image tampering and highlight altered regions using integrity checks.
- **Visible Watermarking**: Overlay visible watermarks using OpenCV.
- 📁 **User-Friendly UI**: Upload images, apply watermark, download, and verify authenticity through a sleek web interface.
- 🔁 **Reverification**: Upload watermarked images again to check if they've been tampered with.

---

## 🛠️ Tech Stack

**Frontend**:
- React (Vite)
- JavaScript
- Axios

**Backend (Flask Microservices)**:
- `flask_backend.py` – Visible watermarking via OpenCV
- `image_watermarking.py` – DCT-based invisible watermarking and tamper detection

**Core Libraries**:
- OpenCV – for image processing and visible watermarking
- NumPy – for matrix manipulation
- SciPy – for applying DCT/IDCT
- PIL (Pillow) – for image format conversion

---

## How It Works

1. **Upload Image** → Apply watermark (visible/invisible)
2. **Download Watermarked Image**
3. **Reupload Image** → Run tamper detection
4. **Get Result**: View whether the image was altered and see the tampered areas (if any)

---

##  Tamper Detection Logic

- Extracts embedded watermark bits from the DCT domain.
- Compares them with the original to check for inconsistencies.
- Highlights differences if tampering is detected.

---

## ⚙️ Local Setup

### Prerequisites

- Python 3.8+
- Node.js 16+

##BACKEND SETUP  

cd backend
pip install -r requirements.txt
python flask_backend.py
# or
python image_watermarking.py

##FRONTEND SETUP
cd frontend
npm install
npm run dev



