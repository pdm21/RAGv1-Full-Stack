import React, { useState } from "react";
import api from "./api"; // Import the Axios instance
import "./App.css"; // Make sure to style your components

function App() {
  const [files, setFiles] = useState([]);
  const [showModal, setShowModal] = useState(false);

  const handleFileUpload = (event) => {
    const uploadedFiles = Array.from(event.target.files);
    setFiles((prevFiles) => [...prevFiles, ...uploadedFiles]);
  };

  const handleRemoveFile = (index) => {
    setFiles((prevFiles) => prevFiles.filter((_, i) => i !== index));
  };

  const toggleModal = () => {
    setShowModal(!showModal);
  };

  const handleSubmit = async () => {
    if (files.length > 0) {
      const formData = new FormData();
      files.forEach((file) => {
        formData.append("file", file);
      });

      try {
        const response = await api.post("/uploadfile/", formData, {
          headers: {
            "Content-Type": "multipart/form-data",
          },
        });
        console.log(response.data);
        // Update the list of uploaded files
        setFiles([]); // Clear files after upload
      } catch (error) {
        console.error("Error uploading file:", error);
      }
    }
  };

  return (
    <div className="app">
      <div className="left-panel">
        <h2>Your documents</h2>
        <div className="upload-section">
          <div className="drop-box">
            <p>Drag and drop files here</p>
            <input type="file" onChange={handleFileUpload} multiple />
            <button onClick={handleSubmit}>Upload</button>
          </div>
          <div className="file-list">
            {files.map((file, index) => (
              <div className="file-item" key={index}>
                <p>{file.name}</p>
                <span>{file.size} bytes</span>
                <button onClick={() => handleRemoveFile(index)}>X</button>
              </div>
            ))}
          </div>
        </div>
      </div>
      <div className="main-panel">
        <h1>Chat with multiple PDFs 📚</h1>
        <input
          type="text"
          placeholder="Enter a query here..."
          className="query-input"
        />
        <div className="response-section"></div>
      </div>
      <div className="info-icon" onClick={toggleModal}>
        ℹ️
      </div>
      {showModal && (
        <div className="modal">
          <div className="modal-content">
            <span className="close-button" onClick={toggleModal}>
              &times;
            </span>
            <h2>About This Application</h2>
            <p>This application was created by Pandelis D. Margaronis.</p>
            <p>Use Case: To upload and query multiple PDF documents.</p>
            <p>Steps to Use:</p>
            <ol>
              <li>
                Upload your PDF files using the drag and drop or browse feature.
              </li>
              <li>Click "Process" to prepare the documents.</li>
              <li>Enter your query in the search box and view the results.</li>
            </ol>
          </div>
        </div>
      )}
    </div>
  );
}

export default App;
