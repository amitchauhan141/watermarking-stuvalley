import React, { useState } from "react";

const ImageUploader = () => {
  const [image, setImage] = useState(null);
  const [watermarkedImageUrl, setWatermarkedImageUrl] = useState("");
  const [originalHash, setOriginalHash] = useState("");
  const [tamperImage, setTamperImage] = useState(null);
  const [tamperResult, setTamperResult] = useState(null);

  const handleWatermarkUpload = async () => {
    const formData = new FormData();
    formData.append("image", image);

    try {
      const res = await fetch("http://127.0.0.1:5001/upload-image", {
        method: "POST",
        body: formData,
      });
      const data = await res.json();
      setWatermarkedImageUrl(data.image_url);
      setOriginalHash(data.image_hash);
      alert("Watermark embedded successfully!");
    } catch (err) {
      alert("Upload failed.");
      console.error(err);
    }
  };

  const handleTamperCheck = async () => {
    const formData = new FormData();
    formData.append("image", tamperImage);
    formData.append("original_hash", originalHash);

    try {
      const res = await fetch("http://127.0.0.1:5001/check-tamper", {
        method: "POST",
        body: formData,
      });
      const data = await res.json();
      setTamperResult(data.tampered);
    } catch (err) {
      alert("Tamper check failed.");
      console.error(err);
    }
  };

  return (
    <div style={{ textAlign: "center", marginTop: "30px" }}>
      <h2>Upload Image for Invisible Watermarking</h2>
      <input type="file" onChange={(e) => setImage(e.target.files[0])} />
      <br />
      <button onClick={handleWatermarkUpload}>Upload & Watermark</button>

      {watermarkedImageUrl && (
        <>
          <h3>Watermarked Image</h3>
          <img src={watermarkedImageUrl} alt="watermarked" width="300" />
          <p>SHA256 Hash: {originalHash}</p>

          <h3>Check for Image Tampering</h3>
          <input type="file" onChange={(e) => setTamperImage(e.target.files[0])} />
          <button onClick={handleTamperCheck}>Check Tampering</button>

          {tamperResult !== null && (
            <p style={{ color: tamperResult ? "red" : "green" }}>
              Image is {tamperResult ? "Tampered" : "Authentic"}
            </p>
          )}
        </>
      )}
    </div>
  );
};

export default ImageUploader;
