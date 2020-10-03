import React, { useState, useEffect, useRef } from 'react';
import logo from './logo.svg';
import './App.css';

function App() {
  const [time, setTime] = useState(0)
  const [url, setUrl] = useState(null)
  let fileRef = useRef()
  let textRef = useRef()

  useEffect(() => {
    fetch('/time').then((res) => res.json()).then(data => {
      setTime(data.time)
    })
    const data = {
      'language': 'Python'
    }
    fetch('/test', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json'
        // 'Content-Type': 'application/x-www-form-urlencoded',
      },
      body: JSON.stringify(data) // body data type must match "Content-Type" header
    }).then((res) => res.json()).then(data => {
      console.log('Test response', data)
    })
  }, [])

  const handleUploadImage = (ev) => {
    ev.preventDefault();
    console.log('handleUploadImage', fileRef.files[0], textRef.value)
    const data = new FormData();
    data.append('file', fileRef.files[0]);
    data.append('filename', textRef.value);
    const uploadAndGet = async () => {
      await fetch('/upload', {
        method: 'POST',
        body: data,
      })
      const filepath = '/display/' + fileRef.files[0].name
      await fetch(filepath).then((res) => setUrl(res.url))
    }
    uploadAndGet()
  }

  return (
    <div className="App">
        <p>Current Time: {time} </p>
        <form onSubmit={handleUploadImage}>
          <div>
            <input ref={(ref) => { fileRef = ref; }} type="file" />
          </div>
          <div>
            <input ref={(ref) => {textRef = ref; }} type="text" placeholder="Enter the desired name of file" />
          </div>
          <br />
          <div>
            <button type='submit'>Upload</button>
          </div>
        </form>
        {
          url && (
            <img src={url} />
          )
        }
    </div>
  );
}

export default App;
