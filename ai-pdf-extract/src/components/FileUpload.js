import React, { useState } from 'react';
import axios from 'axios';
import './FileUpload.css';

const FileUpload = () => {
    const [file, setFile] = useState(null);
    const [details, setDetails] = useState({});
    const [error, setError] = useState(null);
    const [loading, setLoading] = useState(false);

    const handleFileChange = (e) => {
        setFile(e.target.files[0]);
    };

    const handleSubmit = async (e) => {
        e.preventDefault();
        const formData = new FormData();
        formData.append('file', file);

        setLoading(true);
        setError(null);

        try {
            const response = await axios.post('http://127.0.0.1:5000/upload', formData, {
                headers: { 'Content-Type': 'multipart/form-data' },
            });
            setDetails(response.data);
        } catch (error) {
            setError('Error uploading file. Please try again later.');
        } finally {
            setLoading(false);
        }
    };

    return (
        <div className="container">
            <div className="card">
                <h1 className="title">PDF Data Extractor</h1>
                <form onSubmit={handleSubmit} className="upload-form">
                    <input type="file" accept=".pdf" onChange={handleFileChange} required className="file-input" />
                    <button type="submit" disabled={loading} className="upload-button">
                        {loading ? 'Uploading...' : 'Upload'}
                    </button>
                </form>

                {error && <p className="error-message">{error}</p>}

                {details.Name || details.Phone || details.Address ? (
                    <div className="details-container">
                        <h2>Extracted Details</h2>
                        <p><strong>Name:</strong> {details.Name || 'Not found'}</p>
                        <p><strong>Phone Number:</strong> {details.Phone || 'Not found'}</p>
                        <p><strong>Address:</strong> {details.Address || 'Not found'}</p>
                    </div>
                ) : null}
            </div>
        </div>
    );
};

export default FileUpload;
