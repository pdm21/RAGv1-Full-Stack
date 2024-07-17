import React, { useState } from "react";
import api from "./api"; // Import the Axios instance
import "./App.css"; // Make sure to style your components

function App() {
  const [files, setFiles] = useState([]);
  const [showModal, setShowModal] = useState(false);
  const [query, setQuery] = useState("");
  const [messages, setMessages] = useState([]); // state to keep track of conversation history

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
        formData.append("files", file);
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

        // Populate the database
        await api.post("/populate_db/", { reset: false });
      } catch (error) {
        console.error("Error uploading file:", error);
      }
    }
  };

  const handleQuery = async () => {
    try {
      const response = await api.post("/query/", { query });
      const responseText = response.data.response || response.data.error;

      // Splitting the response by "Sources: "
      const splitIndex = responseText.indexOf("Sources:");
      const mainResponse = responseText.substring(0, splitIndex);
      let sources = responseText.substring(splitIndex);

      // Format the sources string
      sources = sources.replace("Sources:", "");
      sources = sources.replace(/\['|'\]/g, "").replace(/', '/g, "\n");
      sources = sources
        .split("\n")
        .map((source) => source.replace("data/", ""))
        .filter((source) => source.trim() !== "");

      setMessages((prevMessages) => [
        ...prevMessages,
        { query, mainResponse, sources, showSources: false },
      ]);
      setQuery(""); // clear the query input after submitting
    } catch (error) {
      console.error("Error fetching query:", error);
    }
  };

  const handleClear = async () => {
    try {
      const response = await api.post("/clearfiles/");
      setMessages([]);
    } catch (error) {
      console.error("Error clearing database and S3:", error);
    }
  };

  return (
    <div className="app">
      <div className="left-panel">
        <h2>Your Documents</h2>
        <div className="upload-section">
          <div className="drop-box">
            <p>Drag and drop files here</p>
            <input
              type="file"
              id="fileUpload"
              onChange={handleFileUpload}
              multiple
            />
            <label htmlFor="fileUpload" className="custom-file-upload">
              Browse Files
            </label>
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
          <div className="upload-button">
            <button onClick={handleSubmit}>Upload</button>
          </div>
        </div>
      </div>

      <div className="main-panel">
        <h1>PDF Document Assistant</h1>
        <div className="query-input-container">
          <input
            type="text"
            placeholder="Enter a query here..."
            className="query-input"
            value={query}
            onChange={(e) => setQuery(e.target.value)}
          />
          <div className="button-container">
            <button className="submit-button" onClick={handleQuery}>
              Submit
            </button>
          </div>
        </div>
        <div
          className="response-section"
          style={{ overflowY: "scroll", height: "400px" }}
        >
          {messages.map((message, index) => (
            <div key={index} className="query-response">
              <div className="query">
                <p>
                  <strong>Q:</strong> {message.query}
                </p>
              </div>
              <div className="response">
                <p>
                  <strong>A:</strong> {message.mainResponse}
                </p>
                {message.showSources && (
                  <div className="sources">
                    <p>
                      <strong>Sources (Page / Chunk):</strong>
                    </p>
                    <ol>
                      {message.sources.map((source, i) => (
                        <li key={i}>{source}</li>
                      ))}
                    </ol>
                    <button
                      onClick={() => {
                        setMessages((prevMessages) => {
                          const newMessages = [...prevMessages];
                          newMessages[index].showSources = false;
                          return newMessages;
                        });
                      }}
                    >
                      Hide Sources
                    </button>
                  </div>
                )}
                {!message.showSources && (
                  <button
                    onClick={() => {
                      setMessages((prevMessages) => {
                        const newMessages = [...prevMessages];
                        newMessages[index].showSources = true;
                        return newMessages;
                      });
                    }}
                  >
                    <em>See Sources</em>
                  </button>
                )}
              </div>
            </div>
          ))}
        </div>

        <div className="clear-button-div">
          <button className="clear-button" onClick={handleClear}>
            Clear
          </button>
        </div>
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
            <p>This application was created by Pandelis Margaronis.</p>
            <p>
              Use Case: LLMs are known for hallucinating results when provided
              with PDF files, whether that involves overlooking user-provided
              context or allowing pre-trained data to influence responses. This
              application aims to solve this problem by utilizing the Retrieval
              Augmented Generation (RAG) techinique. The user may upload and
              query multiple PDF documents, receiving output that is grounded
              solely on the input provided, with the tool providing direct
              citations for all its generated content.
            </p>
            <p>Steps to Use:</p>
            <ol>
              <li>
                Upload your PDF files using the drag and drop or browse feature.
              </li>
              <li>Click "Upload" to upload the documents.</li>
              <li>Enter your query in the search box and click "Submit".</li>
              <li>View the results in the response section.</li>
              <li>
                To start a new conversation with new docs, click "Clear" to
                reset the tool.
              </li>
            </ol>
          </div>
        </div>
      )}
    </div>
  );
}

export default App;
