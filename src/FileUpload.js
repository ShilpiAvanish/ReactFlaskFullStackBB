import React, { useState } from "react";

function FileUpload() {
    const [file, setFile] = useState(null);
    const [responseText, setResponseText] = useState(""); // Updated to handle full text response

    const handleFileChange = (event) => {
        setFile(event.target.files[0]);
    };

    const handleUpload = async () => {
        if (!file) {
            setResponseText("Please select a file.");
            return;
        }

        const formData = new FormData();
        formData.append("file", file);

        try {
            const response = await fetch("http://127.0.0.1:5000/upload", {
                method: "POST",
                body: formData,
            });

            if (!response.ok) {
                throw new Error("Failed to upload file.");
            }

            const data = await response.json();
            console.log(data)
            setResponseText(data.text || data.message); // Updated to display 'text' if available, otherwise 'message'
        } catch (error) {
            setResponseText(error.message);
            console.error("Error uploading file:", error);
        }
    };

    return (
        <div>
            <input type="file" onChange={handleFileChange} />
            <button onClick={handleUpload}>Upload</button>
            {responseText && <p>{responseText}</p>}
        </div>
    );
}

export default FileUpload;
