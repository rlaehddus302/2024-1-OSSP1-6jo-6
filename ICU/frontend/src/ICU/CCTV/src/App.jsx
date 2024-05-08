import classes from './App4.module.css'
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
      <ul className={classes.alarm}>
        {alarm.map((element)=>{
          return (
          <li key={element.id}>
            <p><span className={classes.left}>⚠️{element.camera}번 카메라 노숙취객 탐지 <span className={classes.subText}> 가까운 119 및 112에 신고 요망</span></span><span onClick={() => deletion(event,element.id)} className={classes.right}>❌</span></p>
          </li>)})}
      </ul>
    </>
  )
}

export default App
