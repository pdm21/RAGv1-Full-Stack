import React, { useState } from "react";
import "./App.css"; // Make sure to style your components

function App() {
  // files: An array that holds the uploaded files. Initially, it's an empty array.
  // showModal: A boolean that controls the visibility of the modal. Initially, it's false.
  const [files, setFiles] = useState([]);
  const [showModal, setShowModal] = useState(false);
  /* 
  handleFileUpload: This function is triggered when a file is uploaded. 
  It takes the uploaded files from the event, converts them to an array, 
  and updates the files state by adding the newly uploaded files to the existing ones.
  */
  const handleFileUpload = (event) => {
    const uploadedFiles = Array.from(event.target.files);
    setFiles((prevFiles) => [...prevFiles, ...uploadedFiles]);
  };
  /* 
  handleRemoveFile: This function removes a file from the files 
  array based on its index. It filters out the file at the specified 
  index from the files array.
  */
  const handleRemoveFile = (index) => {
    setFiles((prevFiles) => prevFiles.filter((_, i) => i !== index));
  };
  /* 
  toggleModal: This function toggles the showModal state between true and false, 
  effectively showing or hiding the modal when called.
  */
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
            <p>This application was created by Pandelis Margaronis.</p>
            <p>
              Use Case: To upload and query multiple PDF documents without
              worrying about LLM hallucinations. This tool can be utilized to
              cover reading material, prepare for exams, and identify specific
              content within hundreds / thousands of pages, among other use
              cases.
            </p>
            <p>Three Simple Steps:</p>
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
