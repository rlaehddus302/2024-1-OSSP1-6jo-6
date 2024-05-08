import './App.css'
import Navbar from './Navbar'
import { useRef } from 'react'
import { useState } from 'react'

function App() {
  const [alarm,setAlarm]=useState([{id : 1, camera : 1},{id : 2, camera : 2}]);
  const videoRef = useRef(null);
  const fileInputRef = useRef(null);
  
  function deletion(event,id)
  {
    const correction=alarm.filter((element)=>{
      return(element.id != id)
    })
    console.log(correction)
    setAlarm(correction)
  }
  
  function VideoFileChange(event){
    const file = event.target.files[0];
    const url = URL.createObjectURL(file);
    videoRef.current.src = url;
  }
  return (
    <>
      <Navbar/>

      <ul className='alarm'>
        {alarm.map((element)=>{
          return (
          <li key={element.id}>
            <p><span className='left'>⚠️{element.camera}번 카메라 탐지</span><span onClick={() => deletion(event,element.id)} className='right'>❌</span></p>
          </li>)})}
      </ul>
      <div>
        <h3>Live Video Stream</h3>
        <video ref={videoRef} controls autoPlay>
          <source src='' type='video/mp4'/>
        </video>
      </div>
      <div>
        <h3>Load Video File</h3>
        <input
          type='file'
          ref = {fileInputRef}
          accept='video/*'
          onChange={VideoFileChange}
        />
        <video ref={videoRef} controls>
          <source src='' type='video/mp4'/>
        </video>
      </div>
    </>
  )
}

export default App
