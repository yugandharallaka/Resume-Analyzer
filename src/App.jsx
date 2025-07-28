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
    <div className="min-h-screen bg-gradient-to-br from-gray-900 to-gray-800 text-white flex flex-col items-center px-4 py-10 font-sans">
      <h1 className="text-4xl font-bold mb-8 text-center tracking-tight drop-shadow-lg">
        🧠 AI Resume Analyzer
      </h1>

      <form
        onSubmit={handleSubmit}
        className="bg-white/10 backdrop-blur-md rounded-2xl p-6 w-full max-w-md shadow-xl border border-white/10"
      >
        <label className="block text-sm mb-2 font-medium text-gray-300">Upload your Resume</label>
        <input
          type="file"
          accept=".pdf,.docx"
          onChange={handleFileChange}
          className="w-full text-sm text-gray-100 file:mr-4 file:py-2 file:px-4 file:rounded-lg file:border-0 file:text-sm file:font-semibold file:bg-indigo-500 file:text-white hover:file:bg-indigo-600 cursor-pointer"
        />
        <button
          type="submit"
          className="w-full mt-6 bg-indigo-600 hover:bg-indigo-700 transition-colors text-white py-2 px-4 rounded-lg font-semibold shadow-md"
        >
          🔍 Analyze Resume
        </button>
      </form>

      {result && (
        <div className="mt-10 w-full max-w-3xl bg-white/10 backdrop-blur-md p-6 rounded-2xl border border-white/10 shadow-lg">
          <h2 className="text-2xl font-semibold mb-4">📋 Extracted Information</h2>
          <div className="space-y-2">
            <p><strong>Name:</strong> {result.basic_info.name}</p>
            <p><strong>Email:</strong> {result.basic_info.email}</p>
            <p><strong>Phone:</strong> {result.basic_info.phone}</p>
          </div>

          <h2 className="text-2xl font-semibold mt-6 mb-2">🛠️ Skills</h2>
          <ul className="list-disc list-inside space-y-1 text-sm text-gray-200">
            {result.skills.map((skill, idx) => <li key={idx}>{skill}</li>)}
          </ul>

          <h2 className="text-2xl font-semibold mt-6 mb-2">📂 Domain Recommendation</h2>
          <p className="text-gray-100 text-sm"><strong>{result.domain}</strong></p>

          <h2 className="text-2xl font-semibold mt-6 mb-2">📊 Resume Score</h2>
          <div className="w-full bg-gray-700 rounded-full h-4 overflow-hidden">
            <div
              className="bg-green-500 h-full text-xs text-white text-center transition-all duration-500"
              style={{ width: `${result.score || 0}%` }}
            >
              {result.score || 0}%
            </div>
          </div>

          <h2 className="text-2xl font-semibold mt-6 mb-2">📌 Resume Tips</h2>
          {result.tips.length > 0 ? (
            <ul className="list-disc list-inside text-green-400 text-sm space-y-1">
              {result.tips.map((tip, idx) => <li key={idx}>{tip}</li>)}
            </ul>
          ) : (
            <p className="text-sm text-gray-400">✅ No tips needed — great resume!</p>
          )}
        </div>
      )}
    </div>
  );
}

export default App;
