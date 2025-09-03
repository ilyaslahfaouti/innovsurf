import React, { useState } from 'react';
import './DragAndDrop.css';

const DragAndDrop = ({ onFilesAdded }) => {
    const [dragging, setDragging] = useState(false);
    const [fileList, setFileList] = useState([]);

    const handleDragEnter = (e) => {
        e.preventDefault();
        e.stopPropagation();
        setDragging(true);
    };

    const handleDragLeave = (e) => {
        e.preventDefault();
        e.stopPropagation();
        setDragging(false);
    };

    const handleDragOver = (e) => {
        e.preventDefault();
        e.stopPropagation();
    };

    const handleDrop = (e) => {
        e.preventDefault();
        e.stopPropagation();
        setDragging(false);

        const files = Array.from(e.dataTransfer.files);
        setFileList(prevList => [...prevList, ...files]);
        onFilesAdded(files);
    };

    const handleFileSelect = (e) => {
        const files = Array.from(e.target.files);
        setFileList(prevList => [...prevList, ...files]);
        onFilesAdded(files);
    };

    return (
        <div
            className={`drag-drop-zone ${dragging ? 'dragging' : ''}`}
            onDragEnter={handleDragEnter}
            onDragLeave={handleDragLeave}
            onDragOver={handleDragOver}
            onDrop={handleDrop}
        >
            <p>Drag & drop your files here, or click to select files</p>
            <input
                type="file"
                multiple
                onChange={handleFileSelect}
                className="file-input"
            />
            {fileList.length > 0 && (
                <ul className="file-list">
                    {fileList.map((file, index) => (
                        <li key={index}>{file.name}</li>
                    ))}
                </ul>
            )}
        </div>
    );
};

export default DragAndDrop;
