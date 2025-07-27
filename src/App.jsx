import React, { useState } from 'react';
import axios from 'axios';

function App() {
  const [file, setFile] = useState(null);
  const [result, setResult] = useState(null);

  const handleFileChange = (e) => setFile(e.target.files[0]);

  const handleSubmit = async (e) => {
    e.preventDefault();
    const formData = new FormData();
    formData.append('resume', file);

    try {
      const res = await axios.post('http://localhost:5000/upload', formData);
      setResult(res.data);
    } catch (err) {
      alert("Error: " + err.message);
    }
  };

  return (
    <div className="min-h-screen bg-gray-100 p-4 flex flex-col items-center">
      <h1 className="text-3xl font-bold mb-4">🧠 AI Resume Analyzer</h1>
      
      <form onSubmit={handleSubmit} className="bg-white p-6 rounded-xl shadow-md w-full max-w-md">
        <input
          type="file"
          accept=".pdf"
          onChange={handleFileChange}
          className="block w-full text-sm text-gray-500 file:mr-4 file:py-2 file:px-4 file:border-0 file:text-sm file:font-semibold file:bg-indigo-50 file:text-indigo-700 hover:file:bg-indigo-100"
        />
        <button type="submit" className="mt-4 bg-indigo-600 text-white py-2 px-4 rounded hover:bg-indigo-700">
          Analyze
        </button>
      </form>

      {result && (
        <div className="mt-6 bg-white p-6 rounded-xl shadow-md w-full max-w-2xl">
          <h2 className="text-xl font-semibold">📋 Extracted Information</h2>
          <div className="mt-2 text-sm text-gray-700">
            <p><strong>Name:</strong> {result.basic_info.name}</p>
            <p><strong>Email:</strong> {result.basic_info.email}</p>
            <p><strong>Phone:</strong> {result.basic_info.phone}</p>
          </div>

          <h2 className="text-xl font-semibold mt-4">🛠️ Skills</h2>
          <ul className="list-disc list-inside text-sm text-gray-700">
            {result.skills.map((skill, idx) => <li key={idx}>{skill}</li>)}
          </ul>

          <h2 className="text-xl font-semibold mt-4">📂 Domain Recommendation</h2>
          <p className="text-sm text-gray-700">
            <strong>{result.domain}</strong>
          </p>

          <h2 className="text-xl font-semibold mt-4">📊 Resume Score</h2>
          <div className="mt-1 w-full bg-gray-200 rounded-full h-4 overflow-hidden">
            <div
              className="bg-green-500 h-full text-xs text-white text-center transition-all duration-500"
              style={{ width: `${result.score || 0}%` }}
            >
              {result.score || 0}%
            </div>
          </div>

          <h2 className="text-xl font-semibold mt-4">📌 Resume Tips</h2>
          {result.tips.length > 0 ? (
            <ul className="list-disc list-inside text-sm text-green-700">
              {result.tips.map((tip, idx) => <li key={idx}>{tip}</li>)}
            </ul>
          ) : (
            <p className="text-sm text-gray-600">✅ No tips needed — great resume!</p>
          )}
        </div>
      )}
    </div>
  );
}

export default App;
