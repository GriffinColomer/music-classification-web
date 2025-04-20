import { useState, useRef } from 'react';
import './App.css';

function App() {
  const [file, setFile] = useState(null);
  const [response, setResponse] = useState(null);
  const [recording, setRecording] = useState(false);
  const mediaRecorderRef = useRef(null);
  const audioChunksRef = useRef([]);

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

   const startRecording = async () => {
    const stream = await navigator.mediaDevices.getUserMedia({ audio: true });
    mediaRecorderRef.current = new MediaRecorder(stream);
    audioChunksRef.current = [];

    mediaRecorderRef.current.ondataavailable = (event) => {
      if (event.data.size > 0) {
        audioChunksRef.current.push(event.data);
      }
    };

    mediaRecorderRef.current.onstop = () => {
      const audioBlob = new Blob(audioChunksRef.current, { type: 'audio/webm' });
      const audioFile = new File([audioBlob], 'recording.webm', { type: 'audio/webm' });

      const data = new FormData();
      data.append('file', audioFile);

      const xhr = new XMLHttpRequest();
      xhr.withCredentials = true;

      xhr.onreadystatechange = function () {
        if (xhr.readyState === XMLHttpRequest.DONE) {
          try {
            const jsonResponse = JSON.parse(xhr.responseText);
            setResponse(jsonResponse.genre);
          } catch (error) {
            setResponse('Error processing response');
          }
          console.log(xhr.responseText);
        }
      };

      xhr.open('POST', 'http://localhost:5000/api/sendblob');
      xhr.send(data);

      stream.getTracks().forEach(track => track.stop());
    };

    mediaRecorderRef.current.start();
    setRecording(true);

    setTimeout(() => {
      mediaRecorderRef.current.stop();
      setRecording(false);
    }, 3000);
  };

  return (
    <div className="App">
      <header className="App-header">
        <h1 className="app-title">Real-Time Music Genre Detection</h1>
        <div className="button-container">
          <div className="upload-section">
            <input type="file" accept=".mp3" onChange={handleFileChange} />
            <button onClick={handleUpload}>Send</button>
          </div>
          <div className="record-section">
            <button onClick={startRecording} disabled={recording}>
              {recording ? 'Stop Recording' : 'Start Recording'}
            </button>
          </div>
        </div>
        {response && <p className="genre-response">Genre: {response}</p>}
      </header>
    </div>
  );
}

export default App;