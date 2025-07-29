import React, { useState } from "react";
import axios from "axios";
import {
  FaBrain, FaFileAlt, FaTools, FaFolderOpen, FaChartBar, FaThumbtack
} from "react-icons/fa";
import { CircularProgressbar, buildStyles } from "react-circular-progressbar";
import "react-circular-progressbar/dist/styles.css";
import "./index.css";

const App = () => {
  const [file, setFile] = useState(null);
  const [fileName, setFileName] = useState('');
  const [extractedInfo, setExtractedInfo] = useState(null);
  const [loading, setLoading] = useState(false);

  const handleFileChange = (e) => {
    const selectedFile = e.target.files[0];
    setFile(selectedFile);
    setFileName(selectedFile ? selectedFile.name : '');
  };

  const handleAnalyze = async () => {
    if (!file) {
      alert("Please upload a resume file first.");
      return;
    }

    const formData = new FormData();
    formData.append("resume", file); // must match backend field name

    setLoading(true);
    try {
      const response = await axios.post("http://127.0.0.1:5000/upload", formData);
      setExtractedInfo({
        name: response.data.basic_info.name,
        email: response.data.basic_info.email,
        phone: response.data.basic_info.phone,
        skills: response.data.skills,
        recommended_domain: response.data.domain,
        resume_score: response.data.score,
        tips: response.data.tips
      });
    } catch (error) {
      console.error("Error uploading file:", error);
      alert("Failed to analyze resume.");
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="container">
      <h1><FaBrain /> AI Resume Analyzer</h1>

      {/* Upload Section */}
      <div className="upload-section">
        <label htmlFor="file-upload" className="custom-file-upload">
          📄 Choose Resume
        </label>
        <input
          id="file-upload"
          type="file"
          onChange={handleFileChange}
          accept=".pdf,.doc,.docx"
          style={{ display: "none" }}
        />
        <button onClick={handleAnalyze}>Analyze</button>
      </div>

      {/* File name preview */}
      {fileName && (
        <p style={{ marginTop: '10px', fontSize: '14px', color: '#2c3e50' }}>
          Selected File: <strong>{fileName}</strong>
        </p>
      )}

      {/* Loading state */}
      {loading && <p className="loading">Analyzing resume...</p>}

      {/* Results Section */}
      {extractedInfo && (
        <div className="results">
          <h2><FaFileAlt /> Extracted Information</h2>
          <p><strong>Name:</strong> {extractedInfo.name}</p>
          <p><strong>Email:</strong> {extractedInfo.email}</p>
          <p><strong>Phone:</strong> {extractedInfo.phone}</p>

          <h2><FaTools /> Skills</h2>
          <ul className="skills-list">
            {extractedInfo.skills.map((skill, index) => (
              <li key={index}>{skill}</li>
            ))}
          </ul>

<h2><FaFolderOpen /> Recommended Domain</h2>
<p>Based on your skills, your resume aligns well with:</p>
<div style={{
  display: "inline-block",
  backgroundColor: "#e8f8f5",
  color: "#117864",
  padding: "8px 18px",
  borderRadius: "30px",
  fontWeight: "600",
  fontSize: "16px",
  marginTop: "10px"
}}>
  <b>{extractedInfo.recommended_domain}</b>
</div>


          <h2><FaChartBar /> Resume Score</h2>
          <div className="score-circle">
            <CircularProgressbar
              value={extractedInfo.resume_score}
              text={`${extractedInfo.resume_score}`}
              styles={buildStyles({
                textSize: "24px",
                pathColor: "#1abc9c",
                textColor: "#2c3e50",
                trailColor: "#ecf0f1",
              })}
            />
          </div>

          <h2><FaThumbtack /> Resume Tips</h2>
          <div className="tips-section">
            
            <div className="tips-list">
              {extractedInfo.tips.map((tip, index) => {
                const [intro, skillsPart] = tip.split(":");
                const skills = skillsPart ? skillsPart.split(",").map(s => s.trim()) : [];

                return (
                  <div key={index} className="tip-group text-center">
                    <p className="font-medium">{intro}:</p>
                    <div className="skill-pill-container justify-center">
                      {skills.map((skill, idx) => (
                        <span key={idx} className="skill-pill">{skill}</span>
                      ))}
                    </div>
                  </div>
                );
              })}
            </div>
          </div>
        </div>
      )}
    </div>
  );
};

export default App;
