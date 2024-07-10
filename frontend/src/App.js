import React, { useState } from "react";
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

  return (
    <div className="app">
      {/* 
        Info-Icon in top right corner 
        Provided information on "About this application" and "steps"
      */}
      <div className="info-icon" onClick={toggleModal}>
        ℹ️
      </div>
      {/* Conditional rendering block for when modal is toggled (on-click) */}
      {showModal && (
        <div className="modal">
          <div className="modal-content">
            {/* close button to toggle the modal off and close the pop-up */}
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

      <div className="left-panel">
        <h2>Your documents</h2>
        <div className="upload-section">
          <div className="drop-box">
            <p>Drag and drop files here</p>
            <p></p>
            <input type="file" multiple onChange={handleFileUpload} />
          </div>
          <div className="file-list">
            {files.map((file, index) => (
              <div className="file-item" key={index}>
                <p>{file.name}</p>
                <span>{(file.size / 1024).toFixed(1)}KB</span>
                <button onClick={() => handleRemoveFile(index)}>X</button>
              </div>
            ))}
          </div>
          <button className="process-button">Process</button>
        </div>
      </div>
      <div className="main-panel">
        <h1>Chat with multiple PDFs 📚</h1>
        <input
          type="text"
          placeholder="Enter a query here..."
          className="query-input"
        />
        <div className="response-section">
          <div className="query">
            <p></p>
          </div>
          <div className="response">
            <p></p>
          </div>
        </div>
      </div>
    </div>
  );
}

export default App;
