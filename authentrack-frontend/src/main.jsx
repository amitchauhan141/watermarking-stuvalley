import React from "react";
import ReactDOM from "react-dom/client";
import ImageUploader from "./components/ImageUploader"; // Ensure this file exists
import "./style.css"; // Optional for styling

ReactDOM.createRoot(document.getElementById("root")).render(
  <React.StrictMode>
    <ImageUploader />
  </React.StrictMode>
);
