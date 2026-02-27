import React, { useState } from 'react';
import './App.css'; // Red line hatuna yo line pani thapidiye

const App = () => {
    const [selectedFile, setSelectedFile] = useState(null);
    const [preview, setPreview] = useState(null);
    const [results, setResults] = useState([]);
    const [loading, setLoading] = useState(false);

    const onFileChange = (e) => {
        const file = e.target.files[0];
        if (file) {
            setSelectedFile(file);
            setPreview(URL.createObjectURL(file));
        }
    };

    const onUpload = async () => {
        if (!selectedFile) return alert("Please select an image first!");

        setLoading(true);
        const formData = new FormData();
        formData.append('image', selectedFile);

        try {
            const response = await fetch('http://127.0.0.1:5000/search', {
                method: 'POST',
                body: formData,
            });
            const data = await response.json();

            if (data.status === "success") {
                setResults(data.matches);
            } else {
                alert("Error: " + data.error);
            }
        } catch (err) {
            console.error("Upload failed:", err);
            alert("Backend connected chaina jasto chha!");
        } finally {
            setLoading(false);
        }
    };

    return (
        <div className="min-h-screen bg-gray-50 p-8 font-sans">
            <header className="text-center mb-12">
                <h1 className="text-4xl font-bold text-indigo-700">Wastrika Engine</h1>
                <p className="text-gray-600 mt-2">Visual Search for Clothing</p>
            </header>

            <div className="max-w-2xl mx-auto bg-white p-8 rounded-xl shadow-md border-2 border-dashed border-gray-300">
                <div className="flex flex-col items-center">
                    {preview ? (
                        <img src={preview} alt="Preview" className="h-64 rounded-lg mb-4 object-cover" />
                    ) : (
                        <div className="h-64 flex items-center justify-center text-gray-400">
                            Drag & Drop or Click to Upload
                        </div>
                    )}

                    <input
                        type="file"
                        onChange={onFileChange}
                        className="mb-4 text-sm text-gray-500 file:mr-4 file:py-2 file:px-4 file:rounded-full file:border-0 file:text-sm file:font-semibold file:bg-indigo-50 file:text-indigo-700 hover:file:bg-indigo-100"
                    />

                    <button
                        onClick={onUpload}
                        disabled={loading}
                        className={`w-full py-3 rounded-lg font-bold text-white transition ${loading ? 'bg-gray-400' : 'bg-indigo-600 hover:bg-indigo-700'}`}
                    >
                        {loading ? "Searching..." : "Find Similar Clothes"}
                    </button>
                </div>
            </div>

            <div className="mt-16 max-w-6xl mx-auto">
                <h2 className="text-2xl font-semibold mb-6 text-gray-800">Top Matches</h2>
                <div className="grid grid-cols-1 sm:grid-cols-2 md:grid-cols-3 lg:grid-cols-5 gap-6">
                    {results.map((item, index) => (
                        <div key={index} className="bg-white rounded-xl shadow-lg overflow-hidden border border-gray-100 transform transition hover:scale-105">
                            <img src={item.url} alt="Match" className="w-full h-56 object-cover" />
                            <div className="p-4 text-center">
                                <p className="text-xs font-bold uppercase tracking-wider text-indigo-500 mb-1">
                                    Match #{index + 1}
                                </p>
                                <p className="text-sm text-gray-400 mb-2 italic">
                                    {item.category}
                                </p>
                                <div className="bg-indigo-50 py-1 rounded-full">
                                    <span className="text-lg font-black text-indigo-700">{item.score}</span>
                                    <span className="text-xs text-indigo-400 block">Confidence</span>
                                </div>
                            </div>
                        </div>
                    ))}
                </div>
            </div>
        </div>
    );
};

export default App; // Yo line thapepachi red line jancha!