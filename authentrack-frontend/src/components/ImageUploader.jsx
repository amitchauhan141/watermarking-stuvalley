import React, { useState } from "react";

const ImageUploader = () => {
  const [image, setImage] = useState(null);
  const [watermarkedImage, setWatermarkedImage] = useState("");
  const [watermarkText, setWatermarkText] = useState("AUTHENTRACK");

  const handleImageChange = (e) => {
    setImage(e.target.files[0]);
  };

  const handleWatermark = async () => {
    if (!image) {
      alert("Please select an image.");
      return;
    }

    const formData = new FormData();
    formData.append("file", image);
    formData.append("watermark_text", watermarkText); // Send text watermark

    try {
      const response = await fetch("http://127.0.0.1:5001/upload", {
        method: "POST",
        body: formData,
      });

      const data = await response.json();

      if (response.ok) {
        setWatermarkedImage(data.download_url);
      } else {
        alert("Error: " + data.error);
      }
    } catch (error) {
      alert("Upload failed.");
      console.error("Error:", error);
    }
  };

  return (
    <div style={styles.container}>
      <h2 style={styles.title}>Upload Image & Apply Watermark</h2>

      <input type="file" onChange={handleImageChange} style={styles.fileInput} />

      <input
        type="text"
        value={watermarkText}
        onChange={(e) => setWatermarkText(e.target.value)}
        style={styles.textInput}
        placeholder="Enter watermark text"
      />

      <button onClick={handleWatermark} style={styles.button}>
        Apply Watermark
      </button>

      {watermarkedImage && (
        <div>
          <h3 style={styles.watermarkLabel}>Watermarked Image:</h3>
          <img src={watermarkedImage} alt="Watermarked" style={styles.image} />
          <a href={watermarkedImage} download="watermarked_image.jpg">
            <button style={styles.button}>Download Image</button>
          </a>
        </div>
      )}
    </div>
  );
};

// 🔹 Style object to match your previous UI
const styles = {
  container: {
    textAlign: "center",
    backgroundColor: "#121212",
    color: "white",
    padding: "20px",
    borderRadius: "10px",
    width: "80%",
    margin: "auto",
  },
  title: {
    fontSize: "24px",
    fontWeight: "bold",
  },
  fileInput: {
    margin: "10px 0",
    padding: "10px",
  },
  textInput: {
    width: "80%",
    padding: "10px",
    margin: "10px 0",
    borderRadius: "5px",
    border: "1px solid gray",
  },
  button: {
    backgroundColor: "#000",
    color: "white",
    padding: "10px 20px",
    borderRadius: "5px",
    border: "none",
    cursor: "pointer",
    margin: "10px",
  },
  watermarkLabel: {
    fontSize: "18px",
    fontWeight: "bold",
    marginTop: "20px",
  },
  image: {
    width: "100%",
    maxWidth: "400px",
    borderRadius: "10px",
    margin: "10px 0",
  },
};

export default ImageUploader;
