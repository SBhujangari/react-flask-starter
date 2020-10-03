import React, { useState, useEffect, useRef } from 'react';
import logo from './logo.svg';
import './App.css';
import { Spinner } from 'react-bootstrap';

function App() {
  const [time, setTime] = useState(0)
  const [url, setUrl] = useState(null)
  const [selected, setSelected] = useState('None')
  const [classifying, setClassifying] = useState(false)
  const [prediction, setPrediction] = useState('')
  let fileRef = useRef()

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
    console.log('handleUploadImage', fileRef.files[0])
    const data = new FormData();
    data.append('file', fileRef.files[0]);
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

  const handleChange = (evt) => {
    const filepath = `/display/defaults/${evt.target.value}`
    fetch(filepath).then((res) => setUrl(res.url))
  }

  const run = () => {
    fetch('/classify').then((res) => res.json()).then(data => {
      setPrediction(data.prediction)
    })
  }

  return(
      <div className="App container mt-4">
        <h3 className='display-4 text-center mb-4'>Image Classifier</h3>
        <form class='mb-5 col-8' onSubmit={handleUploadImage}>
          <div class='form-group'>
            <input name='fileUpload' class='form-control-file mb-2' ref={(ref) => { fileRef = ref; }} type="file" />
            <div class='col mb-2 mt-2'>
              <strong class='row'>Image Size should be less than 500kb</strong>
              <strong class='row'>Supported Extensions: PNG, JPG, JPEG, GIF</strong>
            </div>
            <p>If you don't have an image, you can use some of the images below that we've selected.</p> 
            <select class="custom-select" onChange={handleChange}>
              <option selected>Open this select menu</option>
              <option value="1">One</option>
              <option value="2">Two</option>
              <option value="3">Three</option>
            </select>   
          </div>
          <br />
          <div>
            <button type='submit' class="btn btn-primary btn-block" value="Upload">Upload</button>
          </div>
        </form>
        {
          url && (
            <img class='mb-5' src={url} />
          )
        }
        <button class="btn btn-success btn-block" value="Classify" onClick={run}>
          Classify
        </button>
        <h1>{prediction}</h1>
    </div>
  );
}

export default App;
