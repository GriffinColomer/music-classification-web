import { useState } from 'react';
import './App.css';

function App() {
  const [file, setFile] = useState(null);
  const [response, setResponse] = useState(null);

  const handleFileChange = (e) => {
    const selectedFile = setFile(e.target.files[0]);
    // if (selectedFile) {
    //   console.log("Selected file:", {
    //     name: selectedFile.name,
    //     type: selectedFile.type,
    //     size: selectedFile.size + ' bytes',
    //   });
    // };
  }
  const handleUpload = () => {
    if (!file) {
      alert('Please select a file.');
      return;
    }

    const data = new FormData();
    data.append('file', file);
    data.append('user', 'Jelly');
  
    const xhr = new XMLHttpRequest();
    xhr.withCredentials = true;

    xhr.addEventListener("readystatechange", function () {
      if (this.readyState === this.DONE) {
        console.log("Response from server:", this.responseText);
        try {
          const json = JSON.parse(this.responseText);
          setResponse(json.genre);
        } 
        catch {
          setResponse('Invalid response from server');
        }
      }
    });

    xhr.open('POST', 'http://localhost:5000/api/sendmp3');
    xhr.send(data);
  };

  return (
    <div className="App">
      <header className="App-header">
        <input type="file" accept=".mp3" onChange={handleFileChange} />
        <button onClick={handleUpload}>Send</button>
        {response && <p>Genre: {response}</p>}
      </header>
    </div>
  );
}

export default App;