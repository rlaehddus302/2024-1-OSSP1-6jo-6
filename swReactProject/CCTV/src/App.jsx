import './App.css'
import Navbar from './Navbar'
import { useRef } from 'react'
import { useState } from 'react'

function App() {
  const [alarm,setAlarm]=useState([{id : 1, camera : 1},{id : 2, camera : 2}]);
  function deletion(event,id)
  {
    const correction=alarm.filter((element)=>{
      return(element.id != id)
    })
    console.log(correction)
    setAlarm(correction)
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
    </>
  )
}

export default App
